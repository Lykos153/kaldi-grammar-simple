# commands for controlling various programs

try:
    from aenea import *
except:
    from dragonfly import *

gitcommand_array = [
    'add',
    'branch',
    'checkout',
    'clone',
    'commit',
    'diff',
    'fetch',
    'init',
    'log',
    'merge',
    'pull',
    'push',
    'rebase',
    'reset',
    'show',
    'stash',
    'status',
    'tag',
]
gitcommand = {}
for command in gitcommand_array:
    gitcommand[command] = command

class ProgramsRule(MappingRule):
    mapping = {
        "vim save": Key("escape, colon, w, enter"),
        "vim quit": Key("escape, colon, q, enter"),
        "vim really quit": Key("escape, colon, q, exclamation, enter"),
        "vim save and quit": Key("escape, colon, w, q, enter"),
        "vim split": Text(":sp "),
        "vim vertical split": Text(":vs "),
        "vim tab new": Text(":tabnew "),
        "vim tab close": Text(":tabclose\n"),

        "vim open source": Text(":vs %<.c\n"),
        "vim open source plus": Text(":vs %<.cpp\n"),
        "vim open header": Text(":vs %<.h\n") + Key('c-w, c-w'),
        "vim next [tab] [<n>]": Text(':tabnext +%(n)d\n'),
        "vim previous [tab] [<n>]": Text(':tabprevious %(n)d\n'),
        "vim (switch|toggle|swap)": Key('c-w, c-w'),
        "vim rotate": Key('c-w, r'),
        "vim try that": Key('escape, colon, w, enter, a-tab/5, up, enter'),

        'screen': Key('c-a'),
        'screen switch': Key('c-a, c-a'),
        'screen scroll': Key('c-a, lbracket'),

        "just execute": Key("backspace, enter"),
        "command (git|get)": Text("git "),
        "command (git|get) <gitcommand>": Text("git %(gitcommand)s "),
        "command vim": Text("vim "),
        #"command C D": Text("cd "),
        #"command list": Text("ls "),
        "command make": Text("make "),
        "command make clean": Text("make clean "),
        #"command cat": Text("cat "),
        "command (grep|grip)": Text("grep "),
        #"command background": Text("bg "),
        #"command foreground": Text("fg "),

        # web browser
        'address bar': Key('a-d'),
        'refresh page': Key('f5'),
        'really refresh page': Key('s-f5'),
        'go back [<n>]': Key('a-left:%(n)d'),
        'go forward [<n>]': Key('a-right:%(n)d'),
        'previous tab [<n>]': Key('c-pgup:%(n)d'),
        'next tab [<n>]': Key('c-pgdown:%(n)d'),
        'open [new] tab': Key('c-t'),
        'close tab': Key('c-w'),

        # desktop environment commands

        #TODO: how to do this better?
        'workspace one': Key('w-1'),
        'workspace two': Key('w-2'),
        'workspace three': Key('w-3'),
        'workspace four': Key('w-4'),
        'workspace five': Key('w-5'),
        'workspace six': Key('w-6'),
        'workspace seven': Key('w-7)'),
        'workspace eight': Key('w-8)'),
        'workspace nine': Key('w-9'),

        'switch window [<n>]': Key('w-tab:%(n)d'),
        'really close window': Key('ws-q'),
        'maximize window': Key('a-f10'),
        'minimize window': Key('a-f9'),
        'open new terminal': Key('w-enter'),
    }
    extras = [
        Dictation("text"),
        IntegerRef("n", 1, 100),
        Choice('gitcommand', gitcommand),
    ]
    defaults = {
        "n": 1,
    }
