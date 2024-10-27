# Zipper

### Category 

Steganography

### Description

Some data has been hidden somewhere in this archive, good luck finding it!

Format : **Hero{}**<br> 
Author : **Thibz**"

### Files

[secretzip.zip](secretzip.zip)

### Write up

This challenge resides in the fact that we can hide images after a file section right before the 1st central directory header. Then simply update a pointer in an end of central directory record to compensate the shift of the central directory header. When you unzip the archive, the hidden file will be ignored.

We can still see him appear while doing a binwalk.

```bash
$ binwalk -e secretzip.zip 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             Zip archive data, at least v1.0 to extract, name: whatiszip/
68            0x44            Zip archive data, at least v2.0 to extract, compressed size: 31563, uncompressed size: 33944, name: whatiszip/zipheader.png
31712         0x7BE0          Zip archive data, at least v2.0 to extract, compressed size: 27706, uncompressed size: 28510, name: whatiszip/ZIP.pdf
59493         0xE865          Zip archive data, at least v2.0 to extract, compressed size: 29125, uncompressed size: 31304, name: whatiszip/zipformat.png
88699         0x15A7B         PNG image, 1280 x 720, 8-bit/color RGBA, non-interlaced
90037         0x15FB5         Zlib compressed data, default compression
901578        0xDC1CA         End of Zip archive, footer length: 22
```

We can then extract it with foremost

```bash
$> foremost secretzip.zip 
Processing: secretzip.zip
foundat=whatiszip/UT	
foundat=whatiszip/zipheader.pngUT	
foundat=whatiszip/ZIP.pdfUT	
foundat=whatiszip/zipformat.pngUT	

$> cd output/png

$> ls
00000173.png

$> file 00000173.png     
00000173.png: PNG image data, 1280 x 720, 8-bit/color RGBA, non-interlaced
```

The result is an image that looks corrupted, but you can see the flag in the bottom right-hand corner of the image.

![flag](flag.png)

### Flag

```"Hero{Dont_be_fooled_by_appearances}"```