# Transformers #1


## Presentation 

A suspicious file has been found on one of your employee's workstations. He apparently retrieved the .iso file from an e-mail attachment...
Find the file contained in the iso, identify the file type and calculate its sha256 fingerprint.

/!\ WARNING : The content in this challenge can harm your workstation, pls use a sandbox.

ZIP password: InfecteD

Flag : HERO{file-extention;sha256(file)} 
Example : HERO{iso;e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855}

## Write-up

Create a temporary directory to mount the iso file inside and browse file

```
$ mkdir tmp
$ sudo mount ./LINK_FILE_Analysis/img/monthly-report-S3-2024.iso ./tmp
$ ls ./tmp
Document.lnk
```

One file is found. Now calculate the hash (sha256)

```
$ sha256sum ./tmp/Document.lnk 
c3bb38b34c7dfbb1e9e9d588d77f32505184c79cd3628a70ee6df6061e128f3e  tmp/Document.lnk
```

flag : HERO{lnk;c3bb38b34c7dfbb1e9e9d588d77f32505184c79cd3628a70ee6df6061e128f3e}
