************
File formats
************

Input
=====

The JSON and XML formats expect identical data, but in their own particular
formats.

----
JSON
----

This software expects exactly one `data` object at the root. This contains an
object for each donor, indexed by the identifier of the donor. Each donor can
contain a `sources` object, itself a list containing zero, one, or more,
identifiers of recipients paired with this donor.  Each donor object can also
contain a `matches` element, containing a list of match objects, each
containing a `recipient` identifier and a `score` value A donor object can also
contain `dage` (donor age) and `altruistic` keys.  The `altruistic` element,
while used in other software, is not used to mark non-directed donors in
kep_solver. Instead, a donor is non-directed if they are paired with zero
donors.

The following snippet gives an example input file containing two paired donors
(donor 1 paired with recipient 1 and donor 2 paired with recipient 2) as well
as an altruistic donor (donor 3). Donor 3 and donor 1 can donate to recipient
2, and donor 2 can donate to recipient 1.

.. code-block:: json

  { "data" :
      {
      "1" : {
              "sources" : [1],
              "dage" : 65,
              "matches" : [ { "recipient" : 2, "score" : 3 } ]
            },
      "2" : {
              "sources" : [2],
              "dage" : 45,
              "matches" : [ { "recipient" : 1, "score" : 2 } ]
            },
      "3" : {
              "altruistic": true,
              "dage" : 25,
              "matches" : [ { "recipient" : 2, "score" : 1 } ]
            }
      }
  }

---
XML
---

This software expects exactly one `data` tag at the root. This tag will contain
one `entry` tag for each donor, with a `donor_id` attribute storing the
identifier of the donor. Each `entry` tag can contain a `sources` tag, itself
containing zero, one, or more, `source` tags. Text inside each `source` tag
corresponds to the identifier of a recipient paired with this donor.
Each `entry` should also contain a `matches` tag, containing a number of
`match` tags. Each `match` tag contains a `recipient` tag and a `score` tag,
which contain the recipient and score of the match respectively.
An `entry` can also contain `dage` (donor age) and `altruistic` tags. The
`altruistic` tag, while used in other software, is not used to mark
non-directed donors in kep_solver. Instead, a donor is non-directed if they are
paired with zero donors.

The following snippet gives an example input file containing two paired donors
(donor 1 paired with recipient 1 and donor 2 paired with recipient 2) as well
as an altruistic donor (donor 3). Donor 3 and donor 1 can donate to recipient
2, and donor 2 can donate to recipient 1.

.. code-block:: xml

  <?xml version="1.0" ?>
  <data>
      <entry donor_id="1">
      <sources>
        <source>1</source>
      </sources>
      <dage>65</dage>
      <matches>
        <match>
          <recipient>2</recipient>
          <score>3</score>
        </match>
      </matches>
    </entry>
    <entry donor_id="2">
      <sources>
        <source>2</source>
      </sources>
      <dage>58</dage>
      <matches>
        <match>
          <recipient>1</recipient>
          <score>4</score>
        </match>
      </matches>
    </entry>
    <entry donor_id="3">
      <dage>29</dage>
      <altruistic>true</altruistic>
      <matches>
        <match>
          <recipient>2</recipient>
          <score>10</score>
        </match>
      </matches>
    </entry>
  </data>


Output
======

There are currently no proper output formats.

Adding more
===========

Feel free to either file issues on Gitlab or get in touch if you wish to have
more formats added. Include specifics on the file formats
