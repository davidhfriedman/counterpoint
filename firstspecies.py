import sys
import copy
from collections import deque

class Agenda(object):
    """An agenda can be used for depth-first, breadth-first or
    other state-space searches. An agenda has the following
    properties:

    Methods:
       __init__(policy="breadth-first" or "depth-first")
       put(state): add state to the agenda.
       get(): remove and return the next state. Throws exception if empty.
       empty(): true if empty, false if at least one state available.
    """

    BREADTH_FIRST = 1
    DEPTH_FIRST = 2

    def __init__(self, policy):
        """Return an Agenda of policy 'bf' for breadth first and
        'df' for depth first. Raises ValueError for invalid policy"""
        if policy == "breadth-first":
            self.policy = self.BREADTH_FIRST
        elif policy == "depth-first":
            self.policy = self.DEPTH_FIRST
        else:
            raise ValueError("""Agenda invalid policy argument {}
            can be 'breadth-first' or 'depth-first'""".format(policy))
        self.q = deque()

    def __repr__(self):
        return "<Agenda: {} {}>\n".format(len(self.q), self.q)
    
    def put(self, state):
        """Add state to agenda."""
        self.q.appendleft(state)

    def get(self):
        """Remove and return the next state according to policy.
        Raises IndexError if Agenda is empty"""
        if self.empty():
            raise IndexError("""Get from an empty Agenda""")
        else:
            if self.policy == self.BREADTH_FIRST:
                return self.q.pop()
            else:
                return self.q.popleft()

    def empty(self):
        return len(self.q) == 0

# Relative pitches: half-steps above c

(c, d, e, f, g, a, b) = (0, 2, 4, 5, 7, 9, 11)

# The relative pitches of the dorian mode starting on D
#
#           d  e  f  g  a  b   c'    d' e' f' g' a' b' c''
d_dorian = [2, 4, 5, 7, 9, 11, 12]  #14 16 17 19 21 23 24


# The note names of dorian for printing results

notes_in_dorian = ["c", "c#", "d", "d#", "e", "f",
                   "f#", "g", "g#", "a", "a#", "b", "c"]


def note_in_dorian(n):
    """Given a note (pitch_class, octave) display the note name
    and an octave marker. Middle C octave - C4 - no suffix, the
    third octave is C, instead of C3 and the fifth is C' instead
    of C5. Why? 'cuz that's what I'm used to:
    C0...B0 C1...B1 ... C,...B, C...B C'...B' C6...B6 etc."""

    if n == None:  # (None, None):
        return n
    (pitch_class, octave) = n
    s = notes_in_dorian[pitch_class]
    if octave == 0:
        s += '0'
    if octave == 1:
        s += '1'
    if octave == 2:
        s += "2"
    if octave == 3:
        s += ","
    if octave == 5:
        s += "'"
    if octave == 6:
        s += "6"
    if octave == 7:
        s += "7"
    if octave == 8:
        s += "8"
    return s


def maj6((pitch_class, octave)):
    """Return a Note(pitch_class, octave) a major sixth above
       the given Note. Independent of mode."""
    i = pitch_class + 9  # half-steps
    p = i % 12
    o = i / 12
    return (p, octave+o)


def min3((pitch_class, octave)):
    """Return a Note(pitch_class, octave) a minor third above
       the given Note. Independent of mode."""
    i = pitch_class + 3  # half-steps
    p = i % 12
    o = i / 12
    return (p, octave+o)


def interval(p, o, mode, n):
    """Returns the nth note above p,o in the mode."""
    new_pitch = mode.index(p)+(n-1)  # nth note above in mode
    octaves = new_pitch / len(mode)
    ip = mode[new_pitch % len(mode)]
    io = o+octaves
    return (ip, io)


def perfect_consonances((p, o), mode):
    """Returns unison and the fifth and octave above a note."""
    unison = (p, o)
    octave = (p, o+1)
    fifth = interval(p, o, mode, 5)
    return [unison, fifth, octave]


def imperfect_consonances((p, o), mode):
    """Returns the third and sixth above a note."""
    third = interval(p, o, mode, 3)
    sixth = interval(p, o, mode, 6)
    return [third, sixth]


PERFECT = 1
IMPERFECT = 0


def motion(n1, n2):
    """Returns -1,0,1 as n2 is below, equal to, or above n1."""
    (p1, o1) = n1
    (p2, o2) = n2
    if o2 - o1 > 0:
        return 1
    if o2 - o1 < 0:
        return -1
    if p2 - p1 > 0:
        return 1
    if p2 - p1 < 0:
        return -1
    return 0


def eliminate_direct_motion_into_perfect(cf, cp, index, candidates):
    """The rules of counterpoint forbid moving by direct motion into a
    perfect consonance: in other words, no parallel fifths or
    octaves. Contrary (one voice ascends and the other descends) and
    oblique motion (one voice stays on the same note) are always
    allowed."""

    mcf = motion(cf[index], cf[index+1])
    legal = []
    for c in candidates:
        mcp = motion(cp[index], c)
        if mcp != mcf:  # no direct motion into perfect consonance
            legal.append(c)
    return legal


class Counterpoint(object):
    """A Counterpoint consists of a cantus firmus, the mode, the voice (1
    for above, -1 for below) and the current state of the composed
    counterpoint: the notes composed so far, the index of the next
    note to compose, and the counts of perfect and imperfect
    consonances used. The next() method returns a list of all
    next Counterpoints, False if no valid counterpoints, True if
    the composition is finished."""

    ABOVE = 1
    BELOW = -1

    def __init__(self, cf, voice, mode):
        self.cf = cf
        if voice != self.ABOVE and voice != self.BELOW:
            raise ValueError("""Counterpoint voice argument must be
            above {} or below {}, got {}""".format(self.ABOVE, self.BELOW, voice))
        self.voice = voice
        self.mode = mode
        self.len = len(cf)
        self.ult = self.len - 1
        self.penult = self.len - 2
        self.cp = [None for _ in range(self.len)]  # was (None,None)
        # the first note to compose is the penult
        # M6 if cf is the voice above, m3 if below
        self.index = 0  # was self.penult
        self.count_perfect = 0
        self.count_imperfect = 0

        
    def __repr__(self):
        out = "<Counterpoint\n"
        if self.voice == self.ABOVE:
            out += "cp {}\ncf {}"
            top, bot = self.cp, self.cf
        else:
            out += "cf {}\ncp {}"
            top, bot = self.cf, self.cp
        out += "\nlen {} penult {} ult {} index {} voice {} mode {}>\n"
        return out.format(top, bot, self.len, self.penult, self.ult,
                          self.index, self.voice, self.mode)


    def next(self):
        """Return True if done or a list of next
        Counterpoints"""
        
        if self.index == 0:
            # first interval must be a perfect consonance.
            choices = perfect_consonances(self.cf[self.index], self.mode)
            results = []
            for choice in choices:
                k = copy.deepcopy(self)
                k.cp[k.index] = choice
                k.count_perfect += 1
                k.index += 1
                results.append(k)
            return results
        
        if self.index > 0 and self.index < self.penult:
            # prefer more imperfect to perfect intervals,
            # because more interesting
            if self.count_perfect > self.count_imperfect:
                choices = [(c, IMPERFECT) for c in
                           imperfect_consonances(self.cf[self.index],
                                                 self.mode)]
            else:
                choices = [(c, IMPERFECT) for c in
                           imperfect_consonances(self.cf[self.index],
                                                 self.mode)]
                choices += [(c, PERFECT) for c in
                            eliminate_direct_motion_into_perfect(
                                self.cf, self.cp, self.index-1,
                                perfect_consonances(self.cf[self.index],
                                                    self.mode))]
            results = []
            for (choice, type) in choices:
                k = copy.deepcopy(self)
                k.cp[k.index] = choice
                if type == PERFECT:
                    k.count_perfect += 1
                else:
                    k.count_imperfect += 1
                k.index += 1
                results.append(k)
            return results

        if self.index == self.penult:
            # penult is fixed: M6 for voice above, m3 for voice below
            k = copy.deepcopy(self)  # probably ok to modify and return self
            if k.voice == 1:
                k.cp[k.penult] = maj6(k.cf[k.penult])
            else:
                k.cp[k.penult] = min3(k.cf[k.penult])
            k.count_imperfect += 1
            k.index += 1
            return [k]

        if self.index == self.ult:
            # last interval must be a perfect consonance.
            choices = eliminate_direct_motion_into_perfect(
                self.cf, self.cp, self.index-1,
                perfect_consonances(self.cf[self.index], self.mode))
            if len(choices) == 0:
                print """ERROR: no indirect motion to perfect consonance possible at {} cf={} cp={}""".format(self.index, self.cf, self.cp)
                return False
            results = []
            for choice in choices:
                k = copy.deepcopy(self)
                k.cp[k.index] = choice
                k.count_perfect += 1
                k.index += 1
                results.append(k)
            return results

        if self.index > self.ult:
            return True

        # TODO: try to avoid large skips, and compensate for
        # skips up to a fifth by contrary skips


def main(cf):
    """Given a cantus firmus, generate all possible two-voice
    first species counterpoints subject to Fux' rules (hard rules
    implemented; soft rules only partially: tries for more imperfect
    than perfect consonances, but does not avoid skips or try to
    keep the line balanced.

    Prints the generated counterpoints with a count in front as a
    diagnostic in case a bug causes dups. Expect output of the form
      N x x x x x
      N x y x x y
    and if any of the N's is > 1 there was a dup and therefore a bug."""
    
    cfs = {}
    k = Counterpoint(cf, Counterpoint.ABOVE, d_dorian)
    agenda = Agenda("depth-first")
    agenda.put(k)
    while not agenda.empty():
        k = agenda.get()
        result = k.next()
        if result == False:
            #print "FAILED"
            pass
        elif result == True:
            #print("DONE")
            cf_in_dorian = [note_in_dorian(n) for n in k.cf]
            cp_in_dorian = [note_in_dorian(n) for n in k.cp]
            cf = ' '.join(cp_in_dorian)
            if cf in cfs:
                cfs[cf] += 1
            else:
                cfs[cf] = 1
        else:
            for r in result:
                agenda.put(r)
    for key in cfs:
        print cfs[key], key

        
cf = [(n, 4) for n in [d, f, e, d, g, f, a, g, f, e, d]]
#cf = [(n, 4) for n in [d, e, d]]
main(cf)
