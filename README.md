# Monome Arc for Ardour DAW

## *WIP as of this message being here*

This started with these problems

* I miss old school broadcast mixers with the big round faders
* I miss DB channel control at a resolution higher than MIDI
* I like to use software as a pro broadcast mixer but want a hardware surface

This project uses the pymonome library to interact with a Monome Arc,
mapping each ring's encoder to one of four maximum channels volume faders
in the Ardour DAW. 

It depends on the Ardour OSC control surface to be enabled, and serialoscd
to be running on the same host as Ardour. You will need a Monome Arc. They
are not cheap but look real nice.
