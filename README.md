# MiraiToolkit
A collection of tools for Project Mirai romhacking.

## Dependencies
- Python 3

## Included tools:
- [polaris-'s CTPKTool](https://github.com/polaris-/ctpktool) for extracting and modifying CTR Texture files
- [Nutzer's HamiMuCompose tools](https://github.com/Nutzer/HamiMuComposeIII) (both original and new version) for editing the game's song charts **(Windows only)**
- A custom tool made by /u/betasequence on Reddit for extracting individual CTPK files from the game's spr_ae files (which contain multiple textures each). [Can be found on Github here](https://github.com/josephacall/read_ctpk)
- Ohana3DS (Original, not Rebirth) for model/texture import/export (For the obj\_\* files in the nwbin folder) **(Windows only)**
- LoopingAudioConverter for easy BCSTM conversion **(Windows only)**
- [Every File Explorer](https://github.com/Gericom/EveryFileExplorer)
- A text file I made that includes a list of all the songs and their accompanying filenames.

More will be added in the future.

# CTPKTool

**How to use:**
1. Place your ctpk file in the same directory as the ctpktool.exe.
2. Open a command window and navigate to the ctpktool directory.
3. To extract, type ```ctpktool -x <filename>```
4. Edit your file
5. To repack, type ```ctpktool -c <filename>```

# Nutzer's DSC Editors
For this, I highly recommend learning and using the original, as it's more stable and works guaranteed. The newer version doesn't work as well in my experience. It functions, but I can never get it to save without nuking whatever notes I added (as well as everything else).

Instructions for this will come later. It's compliacted and I'm lazy.

# Betasequence's CTPK Extractor
\*Requires Python3 and a hex editor (I like [HxD](https://mh-nexus.de/en/hxd/))

This tool is made to take Project Mirai's spr_ae files (found in the aet_en folder of the game's romfs) and extract all the individual ctpk files from each .bin file. Since each .bin file contains multiple ctpk files, you'd normally have to use a hex editor to extract them all by hand, but this tool makes it super easy.

**Usage:**
1. Place the spr_ae_whatever.bin file you want to extract in the same directory as the tool
2. Open a command window and navigate to the same folder
3. Run ```python3 read.py <filename>```, making sure to also type the extension
4. The tool will extract the individual ctpk files into a new folder. You don't have to change the extension to .ctpk, just keep it as it is already.
5. Use CTPKTool on the extracted ctpk files to get the textures out and modify them to your liking, then repack them.
6. Open the original file and your modified ctpk file in HxD. Make note of the modified file's extracted filename (.bin_image_0, 1, 2, etc)
7. Look for the CTPK chunk in the file that correcponds to your extracted file. .bin_image_0 is the first CTPK chunk, .bin_image_1 is the second one down, 2 is the third one, etc.
8. Select the entire chunk starting with the C in the CTPK header allll the way down to (but not including) the next CTPK header. This is the original image you extracted.
9. Hit backspace (or ctrl+X if you might need it again) to delete that section, and DON'T MOVE THE CURSOR. Keep it where it is.
10. Open your modified CTPK file and hit ctrl+A, then ctrl+C to copy it.
11. Go back to the original file that you removed the chunk from and hit ctrl+V to paste your modified data. Save the file and test it!

If the game crashes, then take another look at the original file vs the modified one that you pasted your own data into. Find the chunk you pasted in and add/remove zeroes from the end (making sure it's on "Insert" and not "Overwrite" mode) until the size of the two files are **exactly** the same down to the byte.

# Ohana3DS
This is included to open the obj_whatever files in the nwbin folder of the romfs.

Simply open Ohana3DS and drag/drop your file into it. Easy as that! You can now export the files you want to modify, change them, and import them again! This does *not* work with the spr_ae files, which is why Betasequence's extractor was made and CTPKTool was included.

# Looping Audio Converter
This is included to add custom songs.

To use, run the program and open up your .wav file. Make sure BCSTM (**not** BRSTM) is selected from the dropdown. Hit convert, wait a few seconds, and you're done!

# Every File Explorer
This was included just in case you want to look around or test stuff. I don't know what real use it has besides previewing some files, but it's nice to have. Also, it can do bcstm to wav conversion.

# WINE
WINE allows Mac and Linux users to run Windows applications on their machines. However, not all applications work, and I have no Mac to test them with. I included a link to the WINE for MacOS install page, which you will have to install manually.
