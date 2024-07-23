Filename identifiers
====================

- Position 01 is Modality       (01 = full-AV, 02 = video-only, 03 = audio-only).
- Position 02 is Vocal channel  (01 = speech, 02 = song).
- Position 03 is Emotion        (01 = neutral, 02 = calm, 03 = happy, 04 = sad, 05 = angry, 06 = fearful, 07 = disgust, 08 = surprised).
- Position 04 is Intensity      (01 = normal, 02 = strong). NOTE: There is no strong intensity for the 'neutral' emotion.
- Position 05 is Statement      (01 = "Kids are talking by the door", 02 = "Dogs are sitting by the door").
- Position 06 is Repetition     (01 = 1st repetition, 02 = 2nd repetition).
- Position 07 is Actor          (01 to 24. Odd numbered actors are male, even numbered actors are female).

Filename Example: 03-01-06-01-02-01-12.wav
- 03=Audio-only
- 01=Speech
- 06=Fearful
- 01=Normal intensity
- 02=Statement "dogs"
- 01=Repetition 1st
- 12=Actor 12 (then female as the actor ID number is even)