#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Person():
    pid: int
    pname: str

    def __init__(self, pid, pname):
        self.pid = pid
        self.pname = pname+'.com'
