#!/usr/bin/env python

""" analyze code """

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"

import copy

import parser

bot_memory = {}

BOT = 'BOTTOM'
TOP = 'TOP'
NBR = 'NUMBER'

TOP_NBR = 100

class aval:
    type_ = BOT
    value = 0

    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.type_ == NBR:
            return "[type: %s, value: %s]" % (self.type_, self.value)
        else:
            return "[type: %s]" % self.type_

def val_add(val1, val2):
    if val1.type_ == BOT:
        return val2
    elif val2.type_ == BOT:
        return val1
    elif val1.type_ == TOP:
        return val1
    elif val2.type_ == TOP:
        return val2
    else:
        ret = aval(NBR, val1.value + val2.value)
        if ret.value > TOP_NBR:
            ret = aval(TOP, 0)
        return ret

def eval(expr, memory):
    if expr == []:
        return aval(NBR, 0)
    operator = expr[0]
    if operator == 'car':
        if eval(expr[1], memory) > 0:
            return aval(NBR, 1)
        else:
            return aval(NBR, 0)
    elif operator == 'cdr':
        evaled = eval(expr[1], memory)
        if evaled.type_ != NBR:
            return evaled
        if evaled.value > 0:
            return aval(NBR, evaled.value - 1)
        else:
            return aval(NBR, 0)
    elif operator == 'append':
        evaled1 = eval(expr[1], memory)
        evaled2 = eval(expr[2], memory)
        return val_add(evaled1, evaled2)
    elif operator == 'do':
        return aval(NBR, 1)
    elif isinstance(expr, str) and expr in memory:
        return memory[expr]
    elif isinstance(expr, list):
        length = len(expr)
        if length > TOP_NBR:
            return aval(TOP, 0)
        return aval(NBR, length)
    else:
        return aval(BOT, 0)

def notempty(expr, memory):
    evaled = eval(expr, memory)
    if evaled.type_ == NBR and evaled.value == 0:
        return bot_memory
    else:
        return memory

def empty(expr, memory):
    evaled = eval(expr, memory)
    if evaled.type_ == NBR and evaled.value == 0:
        return memory
    else:
        return bot_memory

def val_join(val1, val2):
    if val1.type_ == TOP or val2.type_ == TOP:
        return aval(TOP, 0)
    if val1.type_ == BOT:
        return val2
    if val2.type_ == BOT:
        return val1

    return aval(NBR, max(val1.value, val2.value))

def mem_join(mem1, mem2):
    for key in mem1.keys():
        if key in mem2:
            mem2[key] = val_join(mem1[key], mem2[key])
        else:
            mem2[key] = mem1[key]
    return mem2

def val_lteq(val1, val2):
    if val1.type_ == BOT:
        return True
    if val2.type_ == BOT:
        return False
    if val1.type_ == TOP and val2.type_ == TOP:
        return True
    if val1.type_ == TOP and val2.type_ != TOP:
        return False
    return val1.value <= val2.value

def mem_lteq(m1, m2):
    for key in m1.keys():
        if not key in m2:
            return False

        if not val_lteq(m1[key], m2[key]):
            return False
    return True

fix_called = 0
def fix(f):
    def fix_rec(m):
        mcopy = copy.deepcopy(m)
        m2 = f(m)
        if mem_lteq(m2, mcopy):
            return m2
        else:
            return fix_rec(m2)
    return fix_rec(bot_memory)

def trans(program, memory):
    """ return memory after program """
    if len(program) > 1:
        return trans(program[1:], trans([program[0]], memory))
    cmd = program[0]
    operator = cmd[0]
    operand = cmd[1:]
    if operator == 'let':
        memory[operand[0]] = eval(operand[1], memory)
        return memory
    if operator == 'pass':
        return memory
    elif operator == 'if':
        condition = operand[0]
        true_cmd = operand[1]
        false_cmd = operand[2]
        return mem_join(trans(true_cmd, notempty(condition, memory)),
                        trans(false_cmd, empty(condition, memory)))
        return memory
    elif operator == 'while':
        def f(m):
            return mem_join(memory,
                            trans(operand[1], notempty(operand[0], m)))
        return notempty(operand[0], fix(f))
    print "UNACCEPTABLE!!!!!", cmd
    exit(1)

def analyze(program):
    init_mem = {}
    return trans(program, init_mem)
