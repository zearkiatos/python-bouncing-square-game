import pytest

import esper


@pytest.fixture
def world():
    return esper.World()


@pytest.fixture
def populated_world():
    pop_world = esper.World()
    create_entities(pop_world, 2000)
    return pop_world


def test_world_instantiation(world):
    assert type(world) == esper.World
    assert type(world._next_entity_id) == int
    assert type(world._entities) == dict
    assert type(world._components) == dict
    assert type(world._processors) == list


def test_create_entity(world):
    entity1 = world.create_entity()
    entity2 = world.create_entity()
    assert type(entity1) == int and type(entity2) == int
    assert entity1 < entity2


def test_create_entity_with_components(world):
    entity1 = world.create_entity(ComponentA())
    entity2 = world.create_entity(ComponentB())
    assert world.has_component(entity1, ComponentA) is True
    assert world.has_component(entity1, ComponentB) is False
    assert world.has_component(entity2, ComponentA) is False
    assert world.has_component(entity2, ComponentB) is True


def test_adding_component_to_not_existing_entity_raises_error(world):
    with pytest.raises(KeyError):
        world.add_component(123, ComponentA())


def test_create_entity_and_add_components(world):
    entity1 = world.create_entity()
    world.add_component(entity1, ComponentA())
    world.add_component(entity1, ComponentB())
    assert world.has_component(entity1, ComponentA) is True
    assert world.has_component(entity1, ComponentC) is False


def test_create_entity_and_add_components_with_alias(world):
    entity = world.create_entity()
    world.add_component(entity, ComponentA(), type_alias=ComponentF)
    assert world.has_component(entity, ComponentF) is True
    assert world.component_for_entity(entity, ComponentF).a == -66


def test_delete_entity(world):
    entity1 = world.create_entity()
    world.add_component(entity1, ComponentC())
    entity2 = world.create_entity()
    world.add_component(entity2, ComponentD())
    entity_with_component = world.create_entity()
    world.add_component(entity_with_component, ComponentE())
    empty_entity = world.create_entity()

    assert entity_with_component == 3
    world.delete_entity(entity_with_component, immediate=True)
    with pytest.raises(KeyError):
        world.components_for_entity(entity_with_component)
    with pytest.raises(KeyError):
        world.delete_entity(999, immediate=True)
    world.delete_entity(empty_entity, immediate=True)


def test_component_for_entity(world):
    entity = world.create_entity()
    world.add_component(entity, ComponentC())
    assert isinstance(world.component_for_entity(entity, ComponentC), ComponentC)
    with pytest.raises(KeyError):
        world.component_for_entity(entity, ComponentD)


def test_components_for_entity(world):
    entity = world.create_entity()
    world.add_component(entity, ComponentA())
    world.add_component(entity, ComponentD())
    world.add_component(entity, ComponentE())
    all_components = world.components_for_entity(entity)
    assert type(all_components) == tuple
    assert len(all_components) == 3
    with pytest.raises(KeyError):
        world.components_for_entity(999)


def test_has_component(world):
    entity1 = world.create_entity()
    entity2 = world.create_entity()
    world.add_component(entity1, ComponentA())
    world.add_component(entity2, ComponentB())
    assert world.has_component(entity1, ComponentA) is True
    assert world.has_component(entity1, ComponentB) is False
    assert world.has_component(entity2, ComponentA) is False
    assert world.has_component(entity2, ComponentB) is True


def test_has_components(world):
    entity = world.create_entity()
    world.add_component(entity, ComponentA())
    world.add_component(entity, ComponentB())
    world.add_component(entity, ComponentC())
    assert world.has_components(entity, ComponentA, ComponentB) is True
    assert world.has_components(entity, ComponentB, ComponentC) is True
    assert world.has_components(entity, ComponentA, ComponentC) is True
    assert world.has_components(entity, ComponentA, ComponentD) is False
    assert world.has_components(entity, ComponentD) is False


def test_get_component(populated_world):
    assert isinstance(populated_world.get_component(ComponentA), list)
    # Confirm that the actually contains something:
    assert len(populated_world.get_component(ComponentA)) > 0, "No Components Returned"

    for ent, comp in populated_world.get_component(ComponentA):
        assert type(ent) == int
        assert type(comp) == ComponentA


def test_get_two_components(populated_world):
    assert isinstance(populated_world.get_components(ComponentD, ComponentE), list)
    # Confirm that the actually contains something:
    assert len(populated_world.get_components(ComponentD, ComponentE)) > 0, "No Components Returned"

    for ent, comps in populated_world.get_components(ComponentD, ComponentE):
        assert type(ent) == int
        assert type(comps) == list
        assert len(comps) == 2

    for ent, (d, e) in populated_world.get_components(ComponentD, ComponentE):
        assert type(ent) == int
        assert type(d) == ComponentD
        assert type(e) == ComponentE


def test_get_three_components(populated_world):
    assert isinstance(populated_world.get_components(ComponentC, ComponentD, ComponentE), list)

    for ent, comps in populated_world.get_components(ComponentC, ComponentD, ComponentE):
        assert type(ent) == int
        assert type(comps) == list
        assert len(comps) == 3

    for ent, (c, d, e) in populated_world.get_components(ComponentC, ComponentD, ComponentE):
        assert type(ent) == int
        assert type(c) == ComponentC
        assert type(d) == ComponentD
        assert type(e) == ComponentE


def test_try_component(world):
    entity1 = world.create_entity(ComponentA(), ComponentB())

    one_item = world.try_component(entity=entity1, component_type=ComponentA)
    assert isinstance(one_item, ComponentA)

    zero_item = world.try_component(entity=entity1, component_type=ComponentC)
    assert zero_item is None


def test_try_components(world):
    entity1 = world.create_entity(ComponentA(), ComponentB())

    one_item = world.try_components(entity1, ComponentA, ComponentB)
    assert isinstance(one_item, list)
    assert len(one_item) == 2
    assert isinstance(one_item[0], ComponentA)
    assert isinstance(one_item[1], ComponentB)

    zero_item = world.try_components(entity1, ComponentA, ComponentC)
    assert zero_item is None


def test_clear_database(populated_world):
    populated_world.clear_database()
    assert len(populated_world._entities) == 0
    assert len(populated_world._components) == 0
    assert len(populated_world._processors) == 0
    assert len(populated_world._dead_entities) == 0
    assert populated_world._next_entity_id == 0


def test_add_processor(populated_world):
    assert len(populated_world._processors) == 0
    correct_processor_a = CorrectProcessorA()
    assert isinstance(correct_processor_a, esper.Processor)
    populated_world.add_processor(correct_processor_a)
    assert len(populated_world._processors) == 1
    assert isinstance(populated_world._processors[0], esper.Processor)


def test_remove_processor(populated_world):
    assert len(populated_world._processors) == 0
    correct_processor_a = CorrectProcessorA()
    populated_world.add_processor(correct_processor_a)
    assert len(populated_world._processors) == 1
    populated_world.remove_processor(CorrectProcessorB)
    assert len(populated_world._processors) == 1
    populated_world.remove_processor(CorrectProcessorA)
    assert len(populated_world._processors) == 0


def test_get_processor(world):
    processor_a = CorrectProcessorA()
    processor_b = CorrectProcessorB()
    processor_c = CorrectProcessorC()

    world.add_processor(processor_a)
    world.add_processor(processor_b)
    world.add_processor(processor_c)

    retrieved_proc_c = world.get_processor(CorrectProcessorC)
    retrieved_proc_b = world.get_processor(CorrectProcessorB)
    retrieved_proc_a = world.get_processor(CorrectProcessorA)
    assert type(retrieved_proc_a) == CorrectProcessorA
    assert type(retrieved_proc_b) == CorrectProcessorB
    assert type(retrieved_proc_c) == CorrectProcessorC


def test_processor_args(world):
    world.add_processor(ArgsProcessor())
    with pytest.raises(TypeError):
        world.process()  # Missing argument
    world.process("arg")


def test_processor_kwargs(world):
    world.add_processor(KwargsProcessor())
    with pytest.raises(TypeError):
        world.process()  # Missing argument
    world.process("spam", "eggs")
    world.process("spam", eggs="eggs")
    world.process(spam="spam", eggs="eggs")
    world.process(eggs="eggs", spam="spam")


def test_clear_cache(populated_world):
    populated_world.clear_cache()


def test_cache_results(world):
    _______ = world.create_entity(ComponentA(), ComponentB(), ComponentC())
    entity2 = world.create_entity(ComponentB(), ComponentC(), ComponentD())
    assert len(list(query for query in world.get_components(ComponentB, ComponentC))) == 2

    world.delete_entity(entity2, immediate=True)
    assert len(list(query for query in world.get_components(ComponentB, ComponentC))) == 1


class TestEntityExists:
    def test_dead_entity(self, world):
        dead_entity = world.create_entity(ComponentB())
        world.delete_entity(dead_entity)
        assert not world.entity_exists(dead_entity)

    def test_not_created_entity(self, world):
        assert not world.entity_exists(123)

    def test_empty_entity(self, world):
        empty_entity = world.create_entity()
        assert world.entity_exists(empty_entity)

    def test_entity_with_component(self, world):
        entity_with_component = world.create_entity(ComponentA())
        assert world.entity_exists(entity_with_component)


class TestRemoveComponent:
    def test_remove_from_not_existing_entity_raises_key_error(self, world):
        with pytest.raises(KeyError):
            world.remove_component(123, ComponentA)

    def test_remove_not_existing_component_raises_key_error(self, world):
        entity = world.create_entity(ComponentB())

        with pytest.raises(KeyError):
            world.remove_component(entity, ComponentA)

    def test_remove_component_with_object_raises_key_error(self, populated_world):
        entity = 2
        component = ComponentD()

        assert populated_world.has_component(entity, type(component))
        with pytest.raises(KeyError):
            populated_world.remove_component(entity, component)

    def test_remove_component_returns_removed_instance(self, world):
        component = ComponentA()
        entity = world.create_entity(component)

        result = world.remove_component(entity, type(component))

        assert result is component

    def test_remove_last_component_leaves_empty_entity(self, world):
        entity = world.create_entity()
        world.add_component(entity, ComponentA())

        world.remove_component(entity, ComponentA)

        assert not world.has_component(entity, ComponentA)
        assert world.entity_exists(entity)

    def test_removing_one_component_leaves_other_intact(self, world):
        component_a = ComponentA()
        component_b = ComponentB()
        component_c = ComponentC()
        entity = world.create_entity(component_a, component_b, component_c)

        world.remove_component(entity, ComponentB)

        assert world.component_for_entity(entity, ComponentA) is component_a
        assert not world.has_component(entity, ComponentB)
        assert world.component_for_entity(entity, ComponentC) is component_c


def test_event_dispatch_no_handlers():
    esper.dispatch_event("foo")
    esper.dispatch_event("foo", 1)
    esper.dispatch_event("foo", 1, 2)
    esper.event_registry.clear()


def test_event_dispatch_one_arg():
    esper.set_handler("foo", myhandler_onearg)
    esper.dispatch_event("foo", 1)
    esper.event_registry.clear()


def test_event_dispatch_two_args():
    esper.set_handler("foo", myhandler_twoargs)
    esper.dispatch_event("foo", 1, 2)
    esper.event_registry.clear()


def test_event_dispatch_incorrect_args():
    esper.set_handler("foo", myhandler_noargs)
    assert pytest.raises(TypeError), esper.dispatch_event("foo")
    esper.event_registry.clear()


def test_set_methoad_as_handler_in_init():

    class MyClass(esper.Processor):

        def __init__(self):
            esper.set_handler("foo", self._my_handler)

        @staticmethod
        def _my_handler():
            print("OK")

        def process(self, dt):
            pass

    _myclass = MyClass()
    esper.dispatch_event("foo")
    esper.event_registry.clear()


def test_set_instance_methoad_as_handler():
    class MyClass(esper.Processor):

        @staticmethod
        def my_handler():
            print("OK")

        def process(self, dt):
            pass

    myclass = MyClass()
    esper.set_handler("foo", myclass.my_handler)
    esper.dispatch_event("foo")
    esper.event_registry.clear()


##################################################
#   Some helper functions and Component templates:
##################################################
def create_entities(world, number):
    for _ in range(number // 2):
        enemy_type_a = world.create_entity()
        world.add_component(enemy_type_a, ComponentA())
        world.add_component(enemy_type_a, ComponentB())
        world.add_component(enemy_type_a, ComponentD())
        world.add_component(enemy_type_a, ComponentE())
        enemy_type_b = world.create_entity()
        world.add_component(enemy_type_b, ComponentC())
        world.add_component(enemy_type_b, ComponentD())
        world.add_component(enemy_type_b, ComponentE())


class ComponentA:
    def __init__(self):
        self.a = -66
        self.b = 9999.99


class ComponentB:
    def __init__(self):
        self.attrib_a = True
        self.attrib_b = False
        self.attrib_c = False
        self.attrib_d = True


class ComponentC:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = None


class ComponentD:
    def __init__(self):
        self.direction = "left"
        self.previous = "right"


class ComponentE:
    def __init__(self):
        self.items = {"itema": None, "itemb": 1000}
        self.points = [a + 2 for a in list(range(44))]


class ComponentF:
    pass


class CorrectProcessorA(esper.Processor):

    def process(self):
        pass


class CorrectProcessorB(esper.Processor):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def process(self):
        pass


class CorrectProcessorC(esper.Processor):

    def process(self):
        pass


class ArgsProcessor(esper.Processor):

    def process(self, spam):
        pass


class KwargsProcessor(esper.Processor):
    def process(self, spam, eggs):
        pass


class IncorrectProcessor:

    def process(self):
        pass


# Event handler templates:

def myhandler_noargs():
    print("OK")


def myhandler_onearg(arg):
    print("Arg:", arg)


def myhandler_twoargs(arg1, arg2):
    print("Args:", arg1, arg2)
