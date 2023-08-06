# -*- coding: utf-8 -*-
import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import BertConfig, BertModel
from transformers import RobertaConfig, RobertaModel    
from torch.nn import CrossEntropyLoss, MSELoss

def mask_tokens(inputs,tokenizer,args):
    """ Prepare masked tokens inputs/labels for masked language modeling: 80% MASK, 10% random, 10% original. """
    labels = inputs.clone()
    # We sample a few tokens in each sequence for masked-LM training (with probability args.mlm_probability defaults to 0.15 in Bert/RoBERTa)
    probability_matrix = torch.full(labels.shape, 0.15).to(inputs.device)
    special_tokens_mask = [tokenizer.get_special_tokens_mask(val, already_has_special_tokens=True) for val in
                           labels.tolist()]
    probability_matrix.masked_fill_(torch.tensor(special_tokens_mask, dtype=torch.bool).to(inputs.device), value=0.0)
    if tokenizer._pad_token is not None:
        padding_mask = labels.eq(tokenizer.pad_token_id)
        probability_matrix.masked_fill_(padding_mask, value=0.0)
        
    masked_indices = torch.bernoulli(probability_matrix).bool()
    labels[~masked_indices] = -100  # We only compute loss on masked tokens

    # 80% of the time, we replace masked input tokens with tokenizer.mask_token ([MASK])
    indices_replaced = torch.bernoulli(torch.full(labels.shape, 0.8)).bool().to(inputs.device) & masked_indices
    inputs[indices_replaced] = tokenizer.convert_tokens_to_ids(tokenizer.mask_token)

    # 10% of the time, we replace masked input tokens with random word
    indices_random = torch.bernoulli(torch.full(labels.shape, 0.5)).bool().to(inputs.device) & masked_indices & ~indices_replaced
    random_words = torch.randint(len(tokenizer)+(2**(args.max_depth+1)-1)*args.n_estimators, labels.shape, dtype=torch.long).to(inputs.device)
    inputs[indices_random] = random_words[indices_random]

    # The rest of the time (10% of the time) we keep the masked input tokens unchanged
    return inputs, labels


class Model(nn.Module):
    def __init__(self, args,tokenizer):
        super(Model, self).__init__()
        self.args = args
        self.tokenizer = tokenizer
        config = BertConfig.from_pretrained(args.pretrained_path)
        #if args.local:
        #    config.num_hidden_layers = 4
        if args.do_test:
            self.bert = BertModel(config)
        else:
            self.bert = BertModel.from_pretrained(args.pretrained_path,config=config)

        self.linear1 = nn.Linear(config.hidden_size*4,2)
        
    def forward(self,text_ids,labels=None,pretrain=False):
        loss_fct = CrossEntropyLoss()
        if pretrain:
            masked_text_ids,masked_lm_labels=mask_tokens(text_ids.clone(),self.tokenizer,self.args)
            encoder_outputs = self.bert(masked_text_ids,attention_mask = masked_text_ids.ne(0))[0]
            masked_mask = masked_lm_labels.view(-1).ne(-100)
            masked_lm_labels = masked_lm_labels.view(-1)[masked_mask]
            encoder_outputs = encoder_outputs.reshape(-1,encoder_outputs.size(-1))[masked_mask]
            prediction_scores = torch.einsum("ac,dc->ad",encoder_outputs,self.bert.embeddings.word_embeddings.weight)
            mlm_loss = loss_fct(prediction_scores, masked_lm_labels) 
            return mlm_loss
        else:
            features = self.bert(text_ids,attention_mask = text_ids.ne(0))[0]

            mask = text_ids.ne(0)
            word_mask = text_ids[:,64:].ne(0)

            vectors = []
            vectors.append(features[:,64])
            vectors.append((features[:,64:] * word_mask[:,:,None]).sum(1) / (word_mask.sum(-1)+1e-10)[:,None])
            vectors.append(features[:,:64].mean(1))
            vectors.append((features * mask[:,:,None]).sum(1) / (mask.sum(-1)+1e-10)[:,None])
            vec = torch.cat(vectors,-1)

            logits = self.linear1(vec)

            if labels is not None:
                
                loss = loss_fct(logits, labels)
                return loss,torch.softmax(logits,-1)
            else:
                return torch.softmax(logits,-1)
