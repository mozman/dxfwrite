#!/usr/bin/env python
#coding:utf-8
# Created: 09.12.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT License

__author__ = "mozman"

import unittest
from dxfwrite.base import DXFAtom, DXFList, dxfstr
from dxfwrite.base import tags2str

class TestDXFAtom(unittest.TestCase):
    def test_group_code_0(self):
        atom = DXFAtom('HEADER', 0)
        self.assertEqual(dxfstr(atom), '  0\nHEADER\n')
        self.assertEqual(dxfstr(atom), tags2str(atom))
        
    def test_group_code_1000(self):    
        atom = DXFAtom ('SECTION', 1000)
        self.assertEqual(dxfstr(atom), '1000\nSECTION\n')
        self.assertEqual(dxfstr(atom), tags2str(atom))
        
class TestDXFList(unittest.TestCase):
    def test_empty_DXFList(self):
        atoms = DXFList()
        self.assertEqual(dxfstr(atoms), '')
        self.assertEqual(dxfstr(atoms), tags2str(atoms))
        
    def test_flat_DXFList(self):
        atoms = DXFList()
        atoms.append(DXFAtom('HEADER'))
        atoms.append(DXFAtom('SECTION', 1))
        self.assertEqual(dxfstr(atoms), '  0\nHEADER\n  1\nSECTION\n')
        result = tags2str(atoms)
        self.assertEqual(dxfstr(atoms), result)

    def test_Sublists(self):
        atoms = DXFList([
            DXFList([ 
                DXFAtom('TAG1'),
                DXFAtom('TAG2'),
                DXFList([ 
                    DXFAtom('TAG14'),
                    DXFAtom('TAG15'),
                    DXFAtom('TAG16'),
                ]),                
                DXFAtom('TAG3'),
            ]),
            DXFList([ 
                DXFAtom('TAG4'),
                DXFAtom('TAG5'),
                DXFAtom('TAG6'),
                DXFList([ 
                    DXFAtom('TAG11'),
                    DXFAtom('TAG12'),
                    DXFAtom('TAG13'),
                ]),                
            ]),
            DXFAtom('TAG7'),
        ])
        self.assertEqual(dxfstr(atoms), tags2str(atoms))

if __name__=='__main__':
    unittest.main()
