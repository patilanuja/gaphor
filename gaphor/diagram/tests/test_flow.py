import unittest
import gaphor.UML as UML
from gaphor.application import Application
from gaphor.diagram import items

class FlowTestCase(unittest.TestCase):
    def setUp(self):
        Application.init(services=['element_factory'])
        self.element_factory = Application.get_service('element_factory')
        self.diagram = self.element_factory.create(UML.Diagram)

    def shutDown(self):
        Application.shutdown()

    def test_flow(self):
        return self.diagram.create(items.FlowItem, subject=self.element_factory.create(UML.ControlFlow))

# vim:sw=4:et:ai
