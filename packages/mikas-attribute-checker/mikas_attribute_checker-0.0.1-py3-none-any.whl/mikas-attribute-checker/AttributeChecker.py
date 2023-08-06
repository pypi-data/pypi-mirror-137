# SPDX-FileCopyrightText: 2022 Mika Silander (mika.silander@iki.fi)
#
# SPDX-License-Identifier: MIT
#
# For info on SPDX, see https://spdx.org

# -*- coding: utf-8 -*-
import re

class AttributeCheckerError(RuntimeError):

    pass


class AbstractAttributeChecker(object):

    raiseexceptions = True

    def __init__(self, *args, **kwargs):
        raise AttributeCheckerError("Class " + str(type(self)) + " defined no __init__ method.")

    # As exceptions may arise from anywhere, would it make sense to implement a (the top class)
    # AbstractChecker.evaluate method that catches any exception and if that happens,
    # returns False as the result of the evaluation? Not that easy : read second comment below.
    def evaluate(self):
        try:
            result = self._evaluate()
            if type(result) == bool:
                return result
            raise AttributeCheckerError(self.__class__.__name__ + "._evaluate() returned a "
                                        + str(type(result)) + ", boolean was expected.")
        except AttributeCheckerError:
            # we always reraise this exception since it indicates a problem in our checker setup, not
            # in the actual attribute values being checked.
            raise
        except Exception as e:
            if self.raiseexceptions:
                raise
            # Hmmm ... we may have a case of Or and Xor where either of the check clauses will always
            # create an exception while the other clause evaluates to valid and is ok.
            # Then, if the other is true, here we will still turn it to false! Not good.
            # This special case only concerns Or and Xor: we implement _evaluate for them separately.
            return False

    def _normalize_to_boolean(self, clause):
        if isinstance(clause, AbstractAttributeChecker):
            return clause.evaluate()
        if type(clause) == bool:
            return clause
        raise RuntimeError("Couldn't evaluate an object of type " + str(type(clause)))

# This class is used to signal problems in the way AttributeChecker is being used
# by the programmer.
# Exceptions raised during normal attribute checks must be signaled with other
# types of exceptions e.g. RuntimeError so as to be able to distinguish exceptions that
# are normal results of (failures in) attribute checks and implementation related exceptions.
# IOW, an attribute check may fail due to a False status returned or an exception
# occurring during the check. If AbstractAttributeChecker.raiseexceptions is False, then
# exceptions happening during runtime checks are turned automatically into False, i.e. they
# are considered failed checks. For development it is recommended to set
# AbstractAttributeChecker.raiseexceptions to True to get insight of the exceptions raised.
class AllAre(AbstractAttributeChecker):

    def __init__(self, value, iterable, checkfunc=lambda x : x):
        self.expectedvalue = value
        isiterable = True
        try:
            itertest = iter(iterable)
        except TypeError:
            if self.raiseexceptions:
                raise
            isiterable = False
        if not isiterable:
            raise AttributeCheckerError("Can't iterate over a parameter of type "
                                        + str(type(iterable)))
        self.iterator = iterable
        self.checkfunc = checkfunc

    def _evaluate(self):
        atleastone = False
        for i in self.iterator:
            atleastone = True
            result = self.checkfunc(i)
            result = self._normalize_to_boolean(result)
            if result != self.expectedvalue:
                return False
        if not atleastone:
            raise AttributeCheckerError("Iterable parameter " + str(type(self.iterator)) + " had no elements")
        return True


class AllTrue(AllAre):

    def __init__(self, *args):
        super().__init__(True, *args)


class AllFalse(AllAre):

    def __init__(self, *args):
        super().__init__(False, *args)


class And(AllTrue):

    def __init__(self, *args):
        if len(args) != 2:
            raise AttributeCheckerError("And requires 2 clauses, got " + str(len(args)))
        super().__init__(args)


class Or(AbstractAttributeChecker):

    def __init__(self, *args):
        if len(args) != 2:
            raise AttributeCheckerError("Or requires 2 clauses, got " + str(len(args)))
        self.clauses = args

    # See note in AbstractAttributeChecker for motivation for why Or and Xor are implemented differently:
    # An exception in the check of either input clause is considered a check failure and turned into False
    # for allowing a final output of OR and Xor.
    def _evaluate(self):
        for clause in self.clauses:
            try:
                clause = super()._normalize_to_boolean(clause)
            except AttributeCheckerError:
                raise
            except Exception:
                if self.raiseexceptions:
                    raise
                clause = False
            if clause:
                return True
        return False


class Xor(AbstractAttributeChecker):

    def __init__(self, *args):
        if len(args) != 2:
            raise AttributeCheckerError("Xor requires 2 clauses, got " + str(len(args)))
        self.clauses = args

    # See note in AbstractAttributeChecker for motivation for why Or and Xor are implemented differently:
    # An exception in the check of either input clause is considered a check failure and turned into False
    # for allowing a final output of OR and Xor.
    def _evaluate(self):
        results = list()
        for clause in self.clauses:
            try:
                result = super()._normalize_to_boolean(clause)
            except AttributeCheckerError:
                raise
            except Exception:
                if self.raiseexceptions:
                    raise
                results.append(False)
                continue
            results.append(clause)
        return False if results[0] == results[1] else True


class Not(AbstractAttributeChecker):

    def __init__(self, *args):
        if len(args) != 1:
            raise AttributeCheckerError("Not requires 1 clause, got " + str(len(args)))
        self.clause = args[0]

    def _evaluate(self):
        try:
            result = super()._normalize_to_boolean(self.clause)
        except AttributeCheckerError:
            raise
        except Exception:
            if self.raiseexceptions:
                raise
            return True
        return False if result else True


class Matches(AbstractAttributeChecker):

    def __init__(self, *args):
        if len(args) != 2:
            raise AttributeCheckerError("Matches requires a regexp and a string, got "
                                        + str(len(args)) + " parameters.")
        for p in args:
            if not isinstance(p, str):
                raise AttributeCheckerError("Matches requires the regexp and the string to be matched as strings, got " + str(type(p)) + ".")
        # May raise an exception if regexp not parseable
        self.regexp = re.compile(args[0])
        self.value = args[1]

    def _evaluate(self):
        return True if self.regexp.match(self.value) else False
