Fobi replacement study
======================

Goal is to make dynamical forms alike Fobi so we can drop it.

Resume
******

* Controller model represent a form controller;
* Controller model holds Slots;
* Slot model represent a field (and possibly further other kind like buttons or text);
* Controller form will save a valid data submit into an Entry;
* Entry model store the user submitted data;

Technically
***********

* Controller form object is built on the go;
* Since of dynamical nature of Controller form, Entry define a generic column structure
  where the data is stored in a JSON field;
* Slot kinds will be a set of slot pre definition which defines field options and also
  stuff for crispy helper and how to manage data;

Problematics
************

* Since user submitted data is stored as JSON and Entry model is a generic holder for
  many various controllers, how to manage stored data when controller is modified ?
  Like a Controller which have A and B fields, some user submitted data has already
  been stored but then controller is modified to remove A field and include a new
  one C ? Then what if further a field A is added again but with different kind or
  goal ?
* How to implement and manage title/label/etc.. translations ?
