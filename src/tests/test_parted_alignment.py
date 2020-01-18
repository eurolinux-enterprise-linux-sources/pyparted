#
# Test cases for the methods in the parted.alignment module itself
#
# Copyright (C) 2009-2011  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): David Cantrell <dcantrell@redhat.com>
#

import _ped
import parted
import unittest
from tests.baseclass import *

# One class per method, multiple tests per class.  For these simple methods,
# that seems like good organization.  More complicated methods may require
# multiple classes and their own test suite.
class AlignmentNewTestCase(unittest.TestCase):
    def setUp(self):
        self.pa = _ped.Alignment(0, 100)

    def runTest(self):
        # Check that not passing args to parted.Alignment.__init__ is caught.
        self.assertRaises(parted.AlignmentException, parted.Alignment)

        # And then the correct ways of creating a parted.Alignment
        a = parted.Alignment(offset=0, grainSize=100)
        self.assert_(isinstance(a, parted.Alignment))

        b = parted.Alignment(PedAlignment=self.pa)
        self.assert_(isinstance(b, parted.Alignment))

        # Test for _ped.Alignment equality
        self.assertTrue(b.getPedAlignment() == self.pa)

class AlignmentGetSetTestCase(unittest.TestCase):
    def setUp(self):
        self.a = parted.Alignment(offset=27, grainSize=49)

    def runTest(self):
        # Test that passing the args to __init__ works.
        self.assert_(isinstance(self.a, parted.Alignment))
        self.assert_(self.a.offset == 27)
        self.assert_(self.a.grainSize == 49)

        # Test that setting directly and getting with getattr works.
        self.a.offset = 10
        self.a.grainSize = 90

        self.assert_(getattr(self.a, "offset") == 10)
        self.assert_(getattr(self.a, "grainSize") == 90)

        # Check that setting with setattr and getting directly works.
        setattr(self.a, "offset", 20)
        setattr(self.a, "grainSize", 80)

        self.assert_(self.a.offset == 20)
        self.assert_(self.a.grainSize == 80)

        # Check that values have the right type.
        self.assertRaises(TypeError, setattr, self.a, "offset", "string")

        # Check that looking for invalid attributes fails properly.
        self.assertRaises(AttributeError, getattr, self.a, "blah")

@unittest.skip("Unimplemented test case.")
class AlignmentIntersectTestCase(unittest.TestCase):
    def runTest(self):
        # TODO
        self.fail("Unimplemented test case.")

@unittest.skip("Unimplemented test case.")
class AlignmentAlignUpTestCase(unittest.TestCase):
    def runTest(self):
        # TODO
        self.fail("Unimplemented test case.")

@unittest.skip("Unimplemented test case.")
class AlignmentAlignDownTestCase(unittest.TestCase):
    def runTest(self):
        # TODO
        self.fail("Unimplemented test case.")

@unittest.skip("Unimplemented test case.")
class AlignmentAlignNearestTestCase(unittest.TestCase):
    def runTest(self):
        # TODO
        self.fail("Unimplemented test case.")

class AlignmentIsAlignedTestCase(RequiresDevice):
    def setUp(self):
        RequiresDevice.setUp(self)
        self.g = parted.Geometry(device=self.device, start=0, length=100)
        self.a = parted.Alignment(offset=10, grainSize=0)

    def runTest(self):
        # Test a couple ways of passing bad arguments.
        self.assertRaises(TypeError, self.a.isAligned, None, 12)
        self.assertRaises(TypeError, self.a.isAligned, self.g, None)

        # Sector must be inside the geometry.
        self.assert_(self.a.isAligned(self.g, 400) == False)

        # If grain_size is 0, sector must be the same as offset.
        self.assert_(self.a.isAligned(self.g, 10) == True)
        self.assert_(self.a.isAligned(self.g, 0) == False)
        self.assert_(self.a.isAligned(self.g, 47) == False)

        # If grain_size is anything else, there's real math involved.
        self.a.grainSize = 5
        self.assert_(self.a.isAligned(self.g, 20) == True)
        self.assert_(self.a.isAligned(self.g, 23) == False)

class AlignmentGetPedAlignmentTestCase(unittest.TestCase):
    def setUp(self):
        self.pa = _ped.Alignment(0, 100)
        self.alignment = parted.Alignment(PedAlignment=self.pa)

    def runTest(self):
        # Test to make sure we get a _ped.Alignment
        self.assert_(isinstance(self.alignment.getPedAlignment(), _ped.Alignment))

        # Test for _ped.Alignment equality
        self.assertTrue(self.alignment.getPedAlignment() == self.pa)

@unittest.skip("Unimplemented test case.")
class AlignmentStrTestCase(unittest.TestCase):
    def runTest(self):
        # TODO
        self.fail("Unimplemented test case.")

# And then a suite to hold all the test cases for this module.
def suite():
    suite = unittest.TestSuite()
    suite.addTest(AlignmentNewTestCase())
    suite.addTest(AlignmentGetSetTestCase())
    suite.addTest(AlignmentIntersectTestCase())
    suite.addTest(AlignmentAlignUpTestCase())
    suite.addTest(AlignmentAlignDownTestCase())
    suite.addTest(AlignmentAlignNearestTestCase())
    suite.addTest(AlignmentIsAlignedTestCase())
    suite.addTest(AlignmentGetPedAlignmentTestCase())
    suite.addTest(AlignmentStrTestCase())
    return suite

s = suite()
if __name__ == "__main__":
    unittest.main(defaultTest='s', verbosity=2)
