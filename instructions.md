# Instructions - 14 June 2026

Our task is to make a system that can help me to record, transcribe, and store audio notes that I make on my phone. We are trying to minimize friction between me speaking and me getting the transcriptions onto my computer. 

The first step is to build an interface for my phone. I think streamlit would be fine - I just need something that I can easily access. 

For the interface; I want to be able to just do a quick record and also to add some context. For example, sometimes, I may make multiple consequtive notes on the same theme. In these cases, I'd want to somehow keep that context. To do this, just have a record button and a text box above it. in between messages, the text box should NOT be cleared unless I do so. There should also be a language button, which toggles between English (default), French, and German 

After recording, the messages should be sent to a NEON db. We need a new one. 

Then, when I open my pc, I will run a script. it will check the Neon Db for new entries. it will distinguish between entries based on the inputs from the interface (so that it knows to keep multiple recordings together). these files should be pulled to my pc and then transcribed. 

For transcription, we will use Voxtral (do some online research to find the documentation). If possible, incorporate the language tags into the transcription prompt. add a .env file and I will add the mistral api key. add a .gitignore and ignore the .env

After transcription, contents should be here: "C:\Users\spatt\Desktop\RemarkableExploit\processed"; follow similar conventions as with the remarkable exploit docs, but indicate in the title that its transcript_date_number. Add the date/time stuff into the .md file, following the remarkable conventions. 

