#! /usr/bin/env python
# -*- coding: latin-1 -*-


from collections import deque, defaultdict
import itertools
import time

import invariants
import pddl
import timers

class BalanceChecker(object):
    def __init__(self, task, reachable_action_params):
        self.predicates_to_add_actions = defaultdict(set)
        self.action_name_to_heavy_action = {}
        for act in task.actions:
            action = self.add_inequality_preconds(act, reachable_action_params)
            too_heavy_effects = []
            create_heavy_act = False
            heavy_act = action
            for eff in action.effects:
                too_heavy_effects.append(eff)
                if eff.parameters: # universal effect
                    create_heavy_act = True
                    too_heavy_effects.append(eff.copy())
                if not eff.literal.negated:
                    predicate = eff.literal.predicate
                    self.predicates_to_add_actions[predicate].add(action)
            if create_heavy_act:
                heavy_act = pddl.Action(action.name, action.parameters,
                                        action.precondition, too_heavy_effects,
                                        action.cost)
            # heavy_act: duplicated universal effects and assigned unique names
            # to all quantified variables (implicitly in constructor)
            self.action_name_to_heavy_action[action.name] = heavy_act

    def get_threats(self, predicate):
        return self.predicates_to_add_actions.get(predicate, set())

    def get_heavy_action(self, action_name):
        return self.action_name_to_heavy_action[action_name]

    def add_inequality_preconds(self, action, reachable_action_params):
        if reachable_action_params is None or len(action.parameters) < 2:
            return action
        inequal_params = []
        combs = itertools.combinations(list(range(len(action.parameters))), 2)
        for pos1, pos2 in combs:
            inequality = True
            for params in reachable_action_params[action.name]:
                if params[pos1] == params[pos2]:
                    inequality = False
                    break
            if inequality:
                inequal_params.append((pos1, pos2))

        if inequal_params:
            precond_parts = list(action.precondition.parts)
            for pos1, pos2 in inequal_params:
                param1 = action.parameters[pos1].name
                param2 = action.parameters[pos2].name
                new_cond = pddl.NegatedAtom("=", (param1, param2))
                precond_parts.append(new_cond)
            precond = action.precondition.change_parts(precond_parts)
            return pddl.Action(action.name, action.parameters, precond,
                               action.effects, action.cost)
        else:
            return action

def get_fluents(task):
    fluent_names = set()
    for action in task.actions:
        for eff in action.effects:
            fluent_names.add(eff.literal.predicate)
    return [pred for pred in task.predicates if pred.name in fluent_names]

def get_initial_invariants(task):
    for predicate in get_fluents(task):
        all_args = list(range(len(predicate.arguments)))
        for omitted_arg in [-1] + all_args:
            order = [i for i in all_args if i != omitted_arg]
            part = invariants.InvariantPart(predicate.name, order, omitted_arg)
            yield invariants.Invariant((part,))

# Input file might be grounded, beware of too many invariant candidates
MAX_CANDIDATES = 100000
MAX_TIME = 300

def take_time():
    # time.clock() deprecated in Python < 3.8 https://bit.ly/3oBIa6c
    try:
        return time.process_time()    # Python 3.8
    except:
        return time.clock()    # Python < 3.8


def find_invariants(task, reachable_action_params):
    candidates = deque(get_initial_invariants(task))
    print(len(candidates), "initial candidates")
    seen_candidates = set(candidates)

    balance_checker = BalanceChecker(task, reachable_action_params)

    def enqueue_func(invariant):
        if len(seen_candidates) < MAX_CANDIDATES and invariant not in seen_candidates:
            candidates.append(invariant)
            seen_candidates.add(invariant)

    start_time = take_time()
    while candidates:
        candidate = candidates.popleft()
        if take_time() - start_time > MAX_TIME:
            print("Time limit reached, aborting invariant generation")
            return
        if candidate.check_balance(balance_checker, enqueue_func):
            yield candidate

def useful_groups(invariants, initial_facts):
    predicate_to_invariants = defaultdict(list)
    for invariant in invariants:
        for predicate in invariant.predicates:
            predicate_to_invariants[predicate].append(invariant)

    nonempty_groups = set()
    overcrowded_groups = set()
    for atom in initial_facts:
        if isinstance(atom, pddl.Assign):
            continue
        for invariant in predicate_to_invariants.get(atom.predicate, ()):
            group_key = (invariant, tuple(invariant.get_parameters(atom)))
            if group_key not in nonempty_groups:
                nonempty_groups.add(group_key)
            else:
                overcrowded_groups.add(group_key)
    useful_groups = nonempty_groups - overcrowded_groups
    for (invariant, parameters) in useful_groups:
        yield [part.instantiate(parameters) for part in invariant.parts]

def get_groups(task, reachable_action_params=None):
    with timers.timing("Finding invariants"):
        invariants = list(find_invariants(task, reachable_action_params))
    with timers.timing("Checking invariant weight"):
        result = list(useful_groups(invariants, task.init))
    return result

if __name__ == "__main__":
    import pddl
    print("Parsing...")
    task = pddl.open()
    print("Finding invariants...")
    for invariant in find_invariants(task):
        print(invariant)
    print("Finding fact groups...")
    groups = get_groups(task)
    for group in groups:
        print("[%s]" % ", ".join(map(str, group)))
