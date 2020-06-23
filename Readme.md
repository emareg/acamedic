# Acamedic – The Academic Dictionary

A small Hunspell dictionary for professional, scientific writing. 

* **High Quality:** based on SCOWL en-US dictionary and thoroughly tested.
* **High Sensitivity:** 
	* removed words such as `thee`, `fatuous`, or `jerk`.
	* less missed errors (but probably more false-positives)
* **Academic Language:** 
	* added words such as `overapproximation`, `whitepaper`, and `bitmask`.
	* select the scientific domains you need during build
* **Easy Install**: available as extension for LibreOffice and Firefox/Thunderbird.



## Getting Started
Download this repository and then decide for which applications you want to install the dictionary:


**Install System-Wide for Hunspell**<br>
* copy `en-Academic.dic` and `en-Academic.aff` to  `/usr/share/hunspell`

**Install LibreOffice Extension**<br>
* Automatic: Download and open [`acamedic-libreoffice.oxt`](addons/acamedic-libreoffice.oxt?raw=true) file in the `addons` folder.
* Manual: 
	* Start LibreOffice and select `Tools → Extension Manager... → Add`. 
	* Open `acamedic-libreoffice.oxt` from the `addons` folder.

**Install Thunderbird Extension**<br>
* Automatic: Download and open [`acamedic-mozilla.xpi`](addons/acamedic-mozilla.xpi?raw=true).
* Manual: 
	* Start Thunderbird and select `Tools → Add-ons → ⚙ → Install Add-on from file`.
	* Open `acamedic-mozilla.xpi` from the `addons` folder.

**Install for Sublime-Text**<br>
Copy `en-Academic.dic` and `en-Academic.aff` to `~/.config/sublime-text-3/Packages/Language - English/`


**Install for Visual Studio Code**<br>
1. Install the extension `denisgerguri.hunspell-spellchecker` (`Ctrl+Shift+P`, type `Ext install`, type `hunspell`)
2. copy `en-Academic.dic` and `en-Academic.aff` to `~/.vscode/extensions/denisgerguri.hunspell-spellchecker-1.0.1/languages/`
3. Follow instructions at https://marketplace.visualstudio.com/items?itemName=denisgerguri.hunspell-spellchecker#adding-new-language





## Contributing Words
The project is in an early stage and you might find many words in your domain that are missing. Please collect them over time and create an issue with your list of words. Again, the idea is to include only words that you use often or rare words that are very distinct and cannot be confused with other terms.



## Building and Testing
The dictionary is constructed from several individual dictionary files in the `src` folder.

* `/base/` contains common words.
* `/academic/` contains special mathematical, technical, chemical, etc. terms.
* `/names/` contains special names starting with capital letter.
* `/codes/` contains keywords of programming languages.





## Motivation for this Dictionary

For spell checking of academic documents, it is not useful if dictionaries include words such as `thee` or `wee`. They will most likely mask a spelling error of the words `the` or `we`. Since they are archaic or words, probably no one is going to write them but rather read them in some historic text fragments. And even if you write them, a spelling error of these words will most likely be masked by other words because instead of `wee` there is `we`, `see`, or `weed`.

Furthermore, the standard dictionaries include a lot of problematic words, such as `wit`, `dome`, or `wont`.



## Creation Process
I have created this dictionary using the following process:

1. Take a very small base dictionary: [SCOWL-20](http://app.aspell.net/create)
2. Manually go through it an remove non-scientific terms
3. Use it to check reference papers 
4. add newly found terms that are in [SCOWL-60](http://app.aspell.net/create)
5. manually check and add further unrecognized terms


#### Terms I have removed
- archaic terms such as `brethren`, `cobbler`, `sod`, `thee`, `thou`, `unto`, `wive`
- inappropriate words such as `cum`, `slut`, `gnome`, `sexy`
- narrative adjectives such as `cunning`, `fatuous`, `fierce`, `ghastly`, `hitherto`, `pompous`, `sheer`
- uncommon words with common alternatives, such as `envisage` (use `envision`), `futile` (use `useless`),  or `horrific` (use `horrible`). 
- colloquial words such as `eh`, `gig`, `hey`, `lad`, `lousy`, `oh`
- words that are very far away from technical contexts, such as `horde`, `hail`, `hog`, `hut`, `lark`, `mummy`, `bigot`
- religious terms such as `heresy`, `sermon`, `sinful`
- words often used to insult: `hypocrite`, `illiterate`, `inane`, `jerk`, `moron`, `snobbery`
- British / Scottish words that sneaked into the US dictionary, such as `lorry`, `nay`, `dole`, `duff`, `dustbin`
- potential mistakes found in SCOWL-20: `cs`, `alias's` (should be `alias'`), also `species's`, `die's`, `elect's`, `feel's`, `want's`

<!-- uncommon with alternatives: `glean`, `greasy`, `havoc` (use `chaos`), `mend` => repair, `smallish` => `small`-->
<!-- - law terms such as `solicitor` -->
<!-- - potential mistakes in SCOWL-95: `uncorrectablely` (search for `ble/[A-Z]*Y`)  -->


### Testing
I do automatic testing on the resulting dictionary file:

- check that there no duplicates or that duplicates are justified, e.g. `clean` can be a verb `clean/SDG` or adjective `clean/YRT`
- run on some reference papers and check that not many words are missing
- check that all words are spelled correctly:
	- using SCOWL-60 and SCOWL-95 dictionary
	- manually double-check all remaining words with 
		- Google
		- [Cambridge Dictionary](https://dictionary.cambridge.org/)
		- [Oxford Dictionary](https://www.oxfordlearnersdictionaries.com/definition/academic)


### Lessons Learned

* the suffixes `-ic` and `-ical` are mostly interchangeable
* words with `-ical` or `-ual` suffix should (normally) have the `/Y` adverb extension.
* words with `-tive` suffix often have `/SYP`
* words should either have `-icity` or `-ness` suffices and these should not have plural forms. E.g. use `simplifications` instead of `simplicities`. 





## Future Plan: Part-of-Speech Encoding

The Hunspell compression could be used to indicate the POS type of a word. For example `/SDG` means that either `s`, `ed` or `ing` can be appended to the word, indicating a regular verb. However, the compression is only concerned with the size and therefore it needs to be checked for confusing suffixes.

Misleading expansion examples:

* `we/DGT` expands to `we`, `wed`, `wing`, and `west`
* `be/DT` expands to `be`, `bed`, and `best`
* `should/RZ` expands to `should` and `shoulder/S`

As a result, I started to encode regular verbs with `/SDG` and nouns with `/MS`, adjectives with `/RT` or `/Y` for the adjective/adverb combination.





