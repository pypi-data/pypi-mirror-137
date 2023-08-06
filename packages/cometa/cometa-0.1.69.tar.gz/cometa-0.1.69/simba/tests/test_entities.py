from unittest import TestCase

import simba.entities.molecule as sem
import simba.io.storage as sis

class Test_entities(TestCase):
    def test_inchi_parsing(self):
        minchi = "InChI=1S/C17H19NO3/c1-18-7-6-17-10-3-5-13(20)16(17)21-15-12(19)4-2-9(14(15)17)8-11(10)18/h2-5,10-11,13,16,19-20H,6-8H2,1H3/t10-,11+,13-,16-,17-/m0/s1"
        vmol = sem.sibMol(minchi)
        self.assertEqual(vmol.get_id(),'BQJCRHHNABKAKU-KBQPJGBKSA-N')


class Test_storage(TestCase):
    def test_storage(self):
        store = sis.Storage()
        store["poney"] = 10
        self.assertIn("poney",store)
        self.assertEqual(store["poney"] ,10)
