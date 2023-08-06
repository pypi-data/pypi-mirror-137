#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import numpy as np
import pickle as pkl
import argparse
import logging
import random
import torch
from sklearn.metrics import precision_recall_curve
from model import Model
from torch.utils.data import DataLoader, SequentialSampler, RandomSampler
from transformers import AdamW, get_linear_schedule_with_warmup
from transformers import BertTokenizer
from torch.utils.data import Dataset
from sklearn import preprocessing
import pandas as pd
import xgboost as xgb
import lightgbm as lgb
from sklearn.feature_extraction.text import CountVectorizer
from scipy import sparse
import jieba

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)

class TextDataset(Dataset):
    def __init__(self, args, data, fea, tokenizer):
        self.args = args
        self.data = data
        self.fea = fea
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)   
    
    def __getitem__(self, i):
        try:
            tokens = ["[CLS]"]+ self.tokenizer.tokenize(self.data[i]['memo_polish'])[:self.args.text_length-2] + ["[SEP]"]
        except:
            tokens = ["[CLS]"]+ self.tokenizer.tokenize("无")[:self.args.text_length-2] + ["[SEP]"]
        text_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        text_ids += [0] * (self.args.text_length-len(text_ids))
        try:
            label = self.data[i]["label"]
        except:
            label = -1
        return torch.tensor(list(self.fea[i])+text_ids,dtype=torch.long), torch.tensor(label,dtype=torch.long)

        
def set_seed(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)    

    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    
def train(args, model, train_dataset, eval_dataset):
    # build dataloader
    train_dataloader = DataLoader(train_dataset, sampler=RandomSampler(train_dataset), 
                                  batch_size=args.train_batch_size)     

    # Prepare optimizer and schedule (linear warmup and decay)
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
         'weight_decay': args.weight_decay},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]
    optimizer = AdamW(optimizer_grouped_parameters, lr=args.lr)
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=len(train_dataset) // args.train_batch_size * args.num_train_epochs*0.1,num_training_steps=len(train_dataset) // args.train_batch_size * args.num_train_epochs)
    
    
    # Train!
    logger.info("***** Running training *****")
    logger.info("  Num examples = %d", len(train_dataset))
    logger.info("  Num Epochs = %d", args.num_train_epochs)
    logger.info("  Instantaneous batch size per GPU = %d", args.train_batch_size// max(args.n_gpu,1))
    logger.info("  Total train batch size = %d", args.train_batch_size )
    logger.info("  optimization steps per epoch = %d", len(train_dataset) // args.train_batch_size)
    logger.info("  Total optimization steps = %d", len(train_dataset) // args.train_batch_size * args.num_train_epochs)
    
    losses = []
    best_score = 0
    model.train()
    eval_steps = len(train_dataloader) // 3
    for idx in range(args.num_train_epochs):
        for step, batch in enumerate(train_dataloader):
            text_ids, labels = (x.to(args.device) for x in batch)
            loss,_ = model(text_ids,labels)
            losses.append(loss.mean().item()) 
            loss.mean().backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), args.max_grad_norm)
            if (step+1) % 100 == 0:
                logger.info("epoch {} step {} loss {}".format(idx, step+1,round(np.mean(losses[-100:]),4)))

            optimizer.step()
            optimizer.zero_grad()
            scheduler.step()  
            
            if (step+1) % eval_steps == 0:
                results = evaluate(args, eval_dataset, model)

                for key, value in results.items():
                    logger.info("  %s = %s", key, round(value,4))  

                if not os.path.exists(args.output_dir):
                        os.makedirs(args.output_dir)  

                if results['score'] > best_score:  
                    best_score=results['score']
                    logger.info("  "+"*"*20)  
                    logger.info("  Best score:%s",round(best_score,4))
                    logger.info("  "+"*"*20)                          

                    model_to_save = model.module if hasattr(model,'module') else model
                    output_dir = os.path.join(args.output_dir, 'bert_model_{}.bin'.format(args.seed))  
                    model_state = model_to_save.state_dict()
                    torch.save(model_state, output_dir)
                    logger.info("Saving model checkpoint to %s", output_dir)  
            
        results = evaluate(args, eval_dataset, model)
        
        for key, value in results.items():
            logger.info("  %s = %s", key, round(value,4))  
            
        if not os.path.exists(args.output_dir):
                os.makedirs(args.output_dir)  
            
        if results['score'] > best_score:  
            best_score=results['score']
            logger.info("  "+"*"*20)  
            logger.info("  Best score:%s",round(best_score,4))
            logger.info("  "+"*"*20)                          
               
            model_to_save = model.module if hasattr(model,'module') else model
            output_dir = os.path.join(args.output_dir, 'bert_model_{}.bin'.format(args.seed))  
            model_state = model_to_save.state_dict()
            torch.save(model_state, output_dir)
            logger.info("Saving model checkpoint to %s", output_dir)  
            
    return best_score

def pretrain(args, model, train_dataset):
    # build dataloader
    train_dataloader = DataLoader(train_dataset, sampler=RandomSampler(train_dataset), 
                                  batch_size=args.train_batch_size)     

    # Prepare optimizer and schedule (linear warmup and decay)
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
         'weight_decay': args.weight_decay},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]
    optimizer = AdamW(optimizer_grouped_parameters, lr=args.lr)
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=len(train_dataset) // args.train_batch_size * args.num_train_epochs*0.2,num_training_steps=len(train_dataset) // args.train_batch_size * args.num_train_epochs)
    
    
    # Train!
    logger.info("***** Running training *****")
    logger.info("  Num examples = %d", len(train_dataset))
    logger.info("  Num Epochs = %d", args.num_train_epochs)
    logger.info("  Instantaneous batch size per GPU = %d", args.train_batch_size// max(args.n_gpu,1))
    logger.info("  Total train batch size = %d", args.train_batch_size )
    logger.info("  optimization steps per epoch = %d", len(train_dataset) // args.train_batch_size)
    logger.info("  Total optimization steps = %d", len(train_dataset) // args.train_batch_size * args.num_train_epochs)
    
    losses = []
    best_score = 0
    model.train()
    for idx in range(args.num_train_epochs):
        for step, batch in enumerate(train_dataloader):
            text_ids, labels = (x.to(args.device) for x in batch)
            loss = model(text_ids,labels,pretrain=True)
            losses.append(loss.mean().item()) 
            loss.mean().backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), args.max_grad_norm)
            if (step+1) % 100 == 0:
                logger.info("epoch {} step {} loss {}".format(idx, step+1,round(np.mean(losses[-100:]),4)))

            optimizer.step()
            optimizer.zero_grad()
            scheduler.step()  

        if not os.path.exists(args.output_dir):
                os.makedirs(args.output_dir)  

        model_to_save = model.module if hasattr(model,'module') else model
        output_dir = os.path.join(args.output_dir, 'pretrain_model.bin')  
        model_state = model_to_save.state_dict()
        torch.save(model_state, output_dir)
        logger.info("Saving model checkpoint to %s", output_dir)  


def calculate_score(pred,gold):
    precision, recall, thresholds = precision_recall_curve(gold, pred)
    score = 0
    for i, p  in enumerate(precision):
        if p>0.9:
            score += 0.4*recall[i]
            break
    for i, p  in enumerate(precision):
        if p>0.85:
            score += 0.3*recall[i]
            break
    for i, p  in enumerate(precision):
        if p>0.80:
            score += 0.3*recall[i]
            break
    return score

def evaluate(args, eval_dataset, model):
    eval_dataloader = DataLoader(eval_dataset, sampler=SequentialSampler(eval_dataset), 
                                  batch_size=args.eval_batch_size)     
    """ evaluate the model """
    # Evaluate!
    logger.info("***** Running evaluation *****")
    logger.info("  Num examples = %d", len(eval_dataset))    
    logger.info("  Total eval batch size = %d", args.eval_batch_size ) 
    model.eval()
    
    losses = []
    labels = []
    preds = []
    for step, batch in enumerate(eval_dataloader):
        text_ids,label = (x.to(args.device) for x in batch)
        with torch.no_grad():
            loss,pred = model(text_ids,label)
            losses.append(loss.mean().item())
            labels.append(label.cpu())
            preds.append(pred[:,1].detach().cpu())
    labels = torch.cat(labels,0).numpy()
    preds = torch.cat(preds,0).numpy()
    model.train()
    return {
        "total_loss": round(np.mean(losses),4),
        "score": round(calculate_score(preds,labels),4),
    }    

def test(args, eval_dataset, model):
    eval_dataloader = DataLoader(eval_dataset, sampler=SequentialSampler(eval_dataset), 
                                  batch_size=args.eval_batch_size,num_workers=3)     
    """ evaluate the model """
    # Evaluate!
    logger.info("***** Running evaluation *****")
    logger.info("  Num examples = %d", len(eval_dataset))    
    logger.info("  Total eval batch size = %d", args.eval_batch_size ) 
    model.eval()
    
    losses = []
    labels = []
    preds = []
    for step, batch in enumerate(eval_dataloader):
        text_ids,label = (x.to(args.device) for x in batch)
        with torch.no_grad():
            pred = model(text_ids)
            preds.append(pred[:,1].detach().cpu())
    preds = torch.cat(preds,0).numpy()
    return preds

def xgb_train(args, train_data):
    # 定义模型
    model = xgb.XGBClassifier(nthread=4, 
                          learning_rate=0.01,    
                          n_estimators=args.n_estimators,       
                          max_depth=args.max_depth,           
                          gamma=0,               
                          subsample=0.9,       
                          colsample_bytree=0.5) 
    
    train_x = np.array(pd.DataFrame([[x["x{}".format(i)] for i in range(480)] for x in train_data]))
    train_y = np.array([x["label"] for x in train_data])
    model.fit(train_x, train_y)
    return model
    

    

def lgb_train(args, train_data, dev_data):
    # 定义模型
    lgb_model = lgb.LGBMClassifier(
            boosting_type="gbdt", num_leaves=256, reg_alpha=0, reg_lambda=0.,
            max_depth=-1, n_estimators=1000, objective='binary', 
            subsample=0.9, colsample_bytree=0.5, subsample_freq=1,
            learning_rate=0.03, random_state=args.seed, n_jobs=10,early_stopping_rounds=50,
        )
    
    train_x = np.array(pd.DataFrame([[x["x{}".format(i)] for i in range(480)] for x in train_data]))
    dev_x = np.array(pd.DataFrame([[x["x{}".format(i)] for i in range(480)] for x in dev_data]))
    
    train_text = []
    for x in train_data:
        try:
            train_text.append(" ".join(jieba.cut(x["memo_polish"],cut_all=False)))
        except:
            train_text.append("")
        
    dev_text = []
    for x in dev_data:
        try:
            dev_text.append(" ".join(jieba.cut(x["memo_polish"],cut_all=False)))
        except:
            dev_text.append("")
    
    cver=CountVectorizer()
    cver.fit(train_text)
    train_a = cver.transform(train_text)
    dev_a = cver.transform(dev_text)
    train_x = sparse.hstack((train_x, train_a))
    dev_x = sparse.hstack((dev_x, dev_a))    
    
    train_y = np.array([x["label"] for x in train_data])
    dev_y = np.array([x["label"] for x in dev_data])
    
    lgb_model.fit(train_x, train_y,eval_set=[(dev_x,dev_y)],verbose=50)
    
    pred = lgb_model.predict_proba(dev_x)[:,1]
    score = calculate_score(pred,dev_y)
    return (cver,lgb_model),score   
    
    
def main():
    parser = argparse.ArgumentParser()
    # Training setting
    parser.add_argument('--train_batch_size', type=int, default=64)
    parser.add_argument('--eval_batch_size', type=int, default=256)
    parser.add_argument('--num_train_epochs', type=int, default=3)
    parser.add_argument('--text_length', type=int, default=128)
    parser.add_argument('--lr', type=float, default=4e-5)
    parser.add_argument('--weight_decay', type=float, default=0)
    parser.add_argument('--max_grad_norm', type=float, default=1.0)
    parser.add_argument('--seed', type=int, default=1234)
    parser.add_argument('--pretrained_path', type=str, default="chinese-macbert-base")
    # Running mode
    parser.add_argument("--do_train", action='store_true')
    parser.add_argument("--do_pretrain", action='store_true')
    parser.add_argument("--do_test", action='store_true')
    parser.add_argument("--local", action='store_true')
    # XGB
    parser.add_argument('--n_estimators', type=int, default=64)
    parser.add_argument('--max_depth', type=int, default=6)
    
    args = parser.parse_args()

    if args.local is False:
        args.train_data_path = '/home/admin/workspace/job/input/train.jsonl'
        args.test_data_path = '/home/admin/workspace/job/input/test.jsonl'
        args.output_dir = '/home/admin/workspace/job/output/'
    else:
        args.train_data_path = '/mnt/atec/train.jsonl'
        args.test_data_path = '/mnt/atec/train.jsonl'
        args.output_dir = 'output/'
        
    logger.info(args)

    # Setup CUDA, GPU 
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    args.n_gpu = torch.cuda.device_count() 
    logger.warning("Process device: %s, n_gpu: %s", device, args.n_gpu)
    args.device = device
    
    # Build model
    tokenizer = BertTokenizer.from_pretrained(args.pretrained_path)

    if args.do_pretrain:
        args.seed = 1234
        set_seed(args)
            
        model = Model(args,tokenizer)   
        model.to(device)    
        max_values = 2**(args.max_depth+1)-1
        model.bert.resize_token_embeddings(len(tokenizer)+max_values*args.n_estimators) 
        
        if os.path.exists("pretrain_models"):
            checkpoint = "{}/pretrain_model.bin".format("pretrain_models")
            model_to_load = model.module if hasattr(model,'module') else model
            model_to_load.load_state_dict(torch.load(checkpoint,map_location=args.device)) 
            logger.info("Reload model from {}".format(checkpoint)) 
                
        data = []
        all_data = []
        with open(args.train_data_path, 'r', encoding='utf-8') as fp:
            for line in fp:
                js = json.loads(line)
                if js["label"] != -1:
                    data.append(js)
                all_data.append(js)
                
        random.shuffle(data)

        train_data = data[:int(len(data)*0.9)]
        
        xgb_model = xgb_train(args,train_data)
        pkl.dump(xgb_model,open("{}/xgb_model.bin".format(args.output_dir),"wb"))
        x = np.array(pd.DataFrame([[x["x{}".format(i)] for i in range(480)] for x in all_data]))
        fea = xgb_model.apply(x)
        
        for i in range(args.n_estimators):
            fea[:,i] += len(tokenizer)+i * max_values
        train_dataset = TextDataset(args,all_data,fea,tokenizer) 
        pretrain(args, model, train_dataset)
        
                    
            
    if args.do_train:
        xgb_model = pkl.load(open("{}/xgb_model.bin".format("pretrain_models"),"rb"))
        data = []
        with open(args.train_data_path, 'r', encoding='utf-8') as fp:
            for line in fp:
                js = json.loads(line)
                if js["label"] != -1:
                    data.append(js)

        #data = data[:2000]
        # read_data  
        lgb_scores = []
        bert_scores = []
        max_values = 2**(args.max_depth+1)-1
        for seed in range(1234,1235):           
            args.seed = seed
            set_seed(args)
            
            random.shuffle(data)

            train_data = data[:int(len(data)*0.9)]
            dev_data = data[int(len(data)*0.9):]


            # BERT
            if seed in [1234]:
                model = Model(args,tokenizer)   
                model.to(device)    
                model.bert.resize_token_embeddings(len(tokenizer)+max_values*args.n_estimators)
                checkpoint = "{}/pretrain_model.bin".format("pretrain_models")
                model_to_load = model.module if hasattr(model,'module') else model
                model_to_load.load_state_dict(torch.load(checkpoint,map_location=args.device)) 
                logger.info("Reload model from {}".format(checkpoint)) 
                
                
                train_x = np.array(pd.DataFrame([[x["x{}".format(i)] for i in range(480)] for x in train_data]))
                dev_x = np.array(pd.DataFrame([[x["x{}".format(i)] for i in range(480)] for x in dev_data]))
                train_fea = xgb_model.apply(train_x)
                dev_fea = xgb_model.apply(dev_x)

                for i in range(args.n_estimators):
                    train_fea[:,i] += len(tokenizer)+i * max_values
                    dev_fea[:,i] += len(tokenizer)+i * max_values

                train_dataset = TextDataset(args,train_data,train_fea,tokenizer)
                dev_dataset = TextDataset(args,dev_data,dev_fea,tokenizer)
                bert_score = train(args, model, train_dataset, dev_dataset)
                bert_scores.append(bert_score)
                logger.info("  bert score = %s", bert_score) 

            # LGB
            lgb_model, lgb_score = lgb_train(args, train_data, dev_data)
            lgb_scores.append(round(lgb_score,4))
            logger.info("  lgb score = %s", lgb_score) 
            pkl.dump(lgb_model,open("{}/lgb_model_{}.bin".format(args.output_dir,args.seed),"wb"))


            
        with open(os.path.join(args.output_dir,"result.json"), 'w') as fp:
            json.dump({"bert_score": bert_scores, "lgb_score": lgb_scores}, fp)
        
    if args.do_test:
        pred_lgb_ensemble = None
        pred_bert_ensemble = None
        pred_ensemble = None
        model = Model(args,tokenizer)   
        model.to(device)  
        max_values = 2**(args.max_depth+1)-1        
        model.bert.resize_token_embeddings(len(tokenizer)+max_values*args.n_estimators)
        
        data = []
        lgb_scores = []
        bert_scores = []
        ensemble_scores = []
        with open(args.test_data_path, 'r', encoding='utf-8') as fp:
            for line in fp:
                js = json.loads(line)
                if "label" not in js:
                    js["label"] = -2
                if js["label"] != -1:
                    data.append(js)
        #data = data[:2000]             
        # read_data
        lgb_seeds = [1234,1235,1236,1237,1238]
        bert_seeds = [1234]
        for seed in set(lgb_seeds+bert_seeds):
            args.seed = seed
            set_seed(args)                 
            if args.local:
                random.shuffle(data)
                test_data = data[int(len(data)*0.9):]     
            else:
                test_data = data
        
        

            # LGB
            if seed in lgb_seeds:
                lgb_model = pkl.load(open("{}/lgb_model_{}.bin".format("models",seed),"rb"))

                test_x = np.array(pd.DataFrame([[x["x{}".format(i)] for i in range(480)] for x in test_data]))
                test_text = []
                for x in test_data:
                    try:
                        test_text.append(" ".join(jieba.cut(x["memo_polish"],cut_all=False)))
                    except:
                        test_text.append("")   

                test_a = lgb_model[0].transform(test_text)
                test_x = sparse.hstack((test_x, test_a))

                lgb_preds = lgb_model[1].predict_proba(test_x)[:,1]
                #if args.local:
                #    lgb_scores.append(round(calculate_score(lgb_preds,np.array([x["label"]  for x in test_data])),4))
                
                if pred_lgb_ensemble is None:
                    pred_lgb_ensemble = lgb_preds/len(lgb_seeds)
                else:
                    pred_lgb_ensemble += lgb_preds/len(lgb_seeds)
                    
            # BERT
            if seed in bert_seeds:
                xgb_model = pkl.load(open("{}/xgb_model.bin".format("pretrain_models"),"rb"))
                checkpoint = "{}/bert_model_{}.bin".format("models",seed)
                model_to_load = model.module if hasattr(model,'module') else model
                model_to_load.load_state_dict(torch.load(checkpoint,map_location=args.device)) 
                logger.info("Reload model from {}".format(checkpoint)) 

                test_x = np.array(pd.DataFrame([[x["x{}".format(i)] for i in range(480)] for x in test_data]))
                test_fea = xgb_model.apply(test_x)

                for i in range(args.n_estimators):
                    test_fea[:,i] += len(tokenizer) + i * max_values

                test_dataset = TextDataset(args,test_data,test_fea,tokenizer)

                bert_preds = test(args, test_dataset, model)
                #if args.local:
                #    bert_scores.append(round(calculate_score(bert_preds,np.array([x["label"]  for x in test_data])),4))

                #if args.local:
                #    ensemble_scores.append(round(calculate_score(lgb_preds*0.6+bert_preds*0.4,np.array([x["label"]  for x in test_data])),4))
                if pred_bert_ensemble is None:
                    pred_bert_ensemble = bert_preds/len(bert_seeds)
                else:
                    pred_bert_ensemble += bert_preds/len(bert_seeds)

               
        #if args.local:
        #    logger.info("  lgb score = %s", lgb_scores)
        #    logger.info("  bert score = %s", bert_scores)
        #    logger.info("  ensemble score = %s", ensemble_scores)
        pred_ensemble = pred_lgb_ensemble * 0.4 + pred_bert_ensemble * 0.6
        prediction = []
        for js,prob in zip(test_data,pred_ensemble):
            prediction.append({"id":js["id"],"label":float(prob)})

        # 预测结果
        with open(os.path.join(args.output_dir,"predictions.jsonl"), 'w') as fp:
            # 将预测结果写入文件中，格式请参考“数据集格式”小节
            for pred in prediction:
                fp.write(json.dumps(pred)+'\n')
            

    return True

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    if main():
        # 训练成功一定要以0方式退出
        sys.exit(0)
    else:
        # 否则-1退出
        sys.exit(1)
