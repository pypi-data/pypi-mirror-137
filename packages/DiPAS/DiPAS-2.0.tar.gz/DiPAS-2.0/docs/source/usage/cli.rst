Command line interface
----------------------

The DiPAS distribution contains a command line interface which can be used to invoke various functionalities:

* Compute Twiss/lattice parameters: ``dipas twiss path/to/script.{madx,py}``
* Compute Orbit Response Matrix (ORM): ``dipas orm path/to/script.{madx,py}``
* Plot lattice: ``dipas plot path/to/script.{madx,py}``
* DiPAS also supports invoking MADX to compute various quantities:

  * MADX: compute Twiss: ``dipas madx twiss path/to/script.madx``
  * MADX: compute ORM: ``dipas madx orm path/to/script.madx``

* Verify results against MADX: ``dipas verify path/to/script.{madx,py}``
* Convert lattices to other representations e.g. HTML: ``dipas convert to html path/to/script.{madx,py} outfile.html``
  The resulting ``outfile.html`` can be viewed and inspected with a web browser.
* Compute the complete set of beam parameters from user input: ``dipas print beam``
  (e.g. ``dipas print beam --particle=proton --energy=1.4``)

Each of the commands supports a variety of options for customization which can be displayed by using ``--help``
(e.g. ``dipas twiss --help``).
