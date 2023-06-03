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
        #"vim go to line <n>": 

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
        'command ranger': Text("ranger "),

        # web browser
        'address bar': Key('a-d'),
        'reload page': Key('f5'),
        'really reload page': Key('s-f5'),
        'go back [<n>]': Key('a-left:%(n)d'),
        'go forward [<n>]': Key('a-right:%(n)d'),
        'previous tab [<n>]': Key('c-pgup:%(n)d'),
        'next tab [<n>]': Key('c-pgdown:%(n)d'),
        'open [new] tab': Key('c-t'),
        'close tab': Key('c-w'),
        'restore tab': Key('cs-t'),

        # vimium
        'open link': Key('escape') + Key('f'),
        'open link in new tab': Key('escape') + Key('F'),
        'open here': Key('escape') + Key('o'),
        'open in new tab': Key('escape') + Key('O'),
        'find in page': Key('c-f'),
        'next match': Key('f3'),
        'previous match': Key('s-f3'),
        'duplicate tab': Key('escape') + Key('y') + Key('t'),
        'toggle mute': Key('a-m'),
        'first input': Key('g') + Key('i'),
        # desktop environment commands

        #TODO: how to do this better?
        'workspace one': Key('w-1'),
        'workspace two': Key('w-2'),
        'workspace three': Key('w-3'),
        'workspace four': Key('w-4'),
        'workspace five': Key('w-5'),
        'workspace six': Key('w-6'),
        'workspace seven': Key('w-7'),
        'workspace eight': Key('w-8)'),
        'workspace nine': Key('w-9'),
        'move to workspace one': Key('ws-1'),
        'move to workspace two': Key('ws-2'),
        'move to workspace three': Key('ws-3'),
        'move to workspace four': Key('ws-4'),
        'move to workspace five': Key('ws-5'),
        'move to workspace six': Key('ws-6'),
        'move to workspace seven': Key('ws-7'),
        'move to workspace eight': Key('ws-8'),
        'move to workspace nine': Key('ws-9'),
        'next window [<n>]': Key('w-tab:%(n)d'),
        'previous window [<n>]': Key('ws-tab:%(n)d'),
        'really close window': Key('ws-q'),
        'left screen': Key('w-w'),
        'main screen': Key('w-e'),
        'right screen': Key('w-r'),
        'move to left screen': Key('ws-w'),
        'move to main screen': Key('ws-e'),
        'move to right screen': Key('ws-r'),
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
