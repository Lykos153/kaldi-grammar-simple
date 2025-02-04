#!/usr/bin/env python3

"""
Command-module loader for Kaldi.

This script is based on 'dfly-loader-wsr.py' written by Christo Butcher and
has been adapted to work with the Kaldi engine instead.

This script can be used to look for Dragonfly command-modules for use with
the Kaldi engine. It scans the directory it's in and loads any ``_*.py`` it
finds.
"""


# TODO Have a simple GUI for pausing, resuming, cancelling and stopping
# recognition, etc

from __future__ import print_function
import os.path
import logging
import sys

from dragonfly import RecognitionObserver, get_engine
from dragonfly import Grammar, MappingRule, Function, Dictation, FuncContext
from dragonfly.loader import CommandModuleDirectory
from dragonfly.log import setup_log

from whisper import whisper_dictation

# --------------------------------------------------------------------------
# Set up basic logging.

if False:
    # Debugging logging for reporting trouble
    logging.basicConfig(level=10)
    logging.getLogger('grammar.decode').setLevel(20)
    logging.getLogger('grammar.begin').setLevel(20)
    logging.getLogger('compound').setLevel(20)
    logging.getLogger('kaldi.compiler').setLevel(10)
else:
    setup_log()

def printfl(*args, **kwargs):
    print(*args, **kwargs, flush=True)

# --------------------------------------------------------------------------
# User notification / rudimentary UI. MODIFY AS DESIRED

# For message in ('sleep', 'wake')
def notify(message):
    if message == 'sleep':
        printfl("Sleeping...")
        # get_engine().speak("Sleeping")
    elif message == 'wake':
        printfl("Awake...")
        # get_engine().speak("Awake")


# --------------------------------------------------------------------------
# Sleep/wake grammar.

sleeping = False

def load_sleep_wake_grammar(initial_awake):
    sleep_grammar = Grammar("sleep")

    def sleep(force=False):
        global sleeping
        if not sleeping or force:
            sleeping = True
            sleep_grammar.set_exclusiveness(True)
        notify('sleep')

    def wake(force=False):
        global sleeping
        if sleeping or force:
            sleeping = False
            sleep_grammar.set_exclusiveness(False)
        notify('wake')

    class SleepRule(MappingRule):
        mapping = {
            "please start listening":  Function(wake) + Function(lambda: get_engine().start_saving_adaptation_state()),
            "stop listening":   Function(lambda: get_engine().stop_saving_adaptation_state()) + Function(sleep),
            "halt listening":   Function(lambda: get_engine().stop_saving_adaptation_state()) + Function(sleep),
        }
    sleep_grammar.add_rule(SleepRule())

    sleep_noise_rule = MappingRule(
        name = "sleep_noise_rule",
        mapping = { "<text>": Function(lambda text: False and print(text)) },
        extras = [ Dictation("text") ],
        context = FuncContext(lambda: sleeping),
    )
    sleep_grammar.add_rule(sleep_noise_rule)

    sleep_grammar.load()

    if initial_awake:
        wake(force=True)
    else:
        sleep(force=True)


# --------------------------------------------------------------------------
# Simple recognition observer class.

class Observer(RecognitionObserver):
    def on_begin(self):
        printfl("Speech started.")

    def on_recognition(self, words):
        printfl("Recognized:", " ".join(words))

    def on_failure(self):
        printfl("Sorry, what was that?")


# --------------------------------------------------------------------------
# Main event driving loop.

def main(args):
    logging.basicConfig(level=logging.INFO)

    path = os.path.dirname(sys.argv[0])
    if path in ("", "-c"):
        printfl("ERROR: Could not find modules")
        exit(1)

    # Set any configuration options here as keyword arguments.
    engine = get_engine("kaldi",
        model_dir='kaldi_model',
        tmp_dir='kaldi_model.tmp',  # default for temporary directory
        # vad_aggressiveness=3,  # default aggressiveness of VAD
        # vad_padding_end_ms=300,  # default ms of required silence surrounding VAD
        # vad_complex_padding_end_ms=1200,
        # input_device_index=None,  # set to an int to choose a non-default microphone
        # auto_add_to_user_lexicon=True,  # set to True to possibly use cloud for pronunciations
        alternative_dictation=whisper_dictation,
    )

    # Call connect() now that the engine configuration is set.
    engine.connect()

    # Register a recognition observer
    observer = Observer()
    observer.register()

    load_sleep_wake_grammar(True)

    directory = CommandModuleDirectory(path, excludes=[__file__])
    directory.load()

    # Start the engine's main recognition loop
    engine.mimic("please start listening")
    engine.prepare_for_recognition()
    try:
        # Loop forever
        printfl("Listening...")
        engine.do_recognition()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main(sys.argv[1:])
