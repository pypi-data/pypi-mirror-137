sphinx-metavar
==============

This is a simple extension to Sphinx_ that adds a missing piece of
semantic markup, namely metasyntactic variables.  It does three things:

- patch the ``:samp:`` role so that it uses more accurate and
  customizable styling for those parts within braces,

- define a ``:metavar:`` role, to refer to these braced parts outside of
  the ``:samp:``,

- define a ``.. samp::`` directive as an easy way to use the
  functionality of ``:samp:`` for an entire block (this part is similar
  to sphinxawesome-sampdirective_, but uses the better markup for
  metasyntactic variables).

In HTML, metasyntactic variables are marked up with italics, just as if
you were using emphasis, except that the ``<em>`` tag has the
``metavar`` class, so you can override the style in CSS.  In plain text,
metasyntactic variables are uppercased.  Texinfo output uses the
``@var{}`` command, which results in italics for HTML and PDF, and
uppercase in Info.  In other formats, metasyntactic variables are
(currently) output the same as emphasis.

Example usage:

.. code-block:: restructuredtext

   Bazing the foo requires a special command, used like:

   .. samp::

      Frobnicate for {xyz}

   where :metavar:`xyz` is your spam of eggs.  If you do not need the eggs,
   you can use the simpler form :samp:`Frobnicate {xyz}`.


Output:

   Bazing the foo requires a special command, used like:

   .. samp::

      Frobnicate for {xyz}

   where :metavar:`xyz` is your spam of eggs.  If you do not need the eggs,
   you can use the simpler form :samp:`Frobnicate {xyz}`.

Observe how the HTML version of this text uses custom CSS styling that
underlines metasyntactic variables.  This is done by adding a
:file:`metavar.css` file (using ``html_css_files = ['metavar.css']`` in
:file:`conf.py`) which contains:

.. code-block:: css

   .metavar {
     text-decoration: underline;
   }

.. _Sphinx: https://www.sphinx-doc.org
.. _sphinxawesome-sampdirective: https://pypi.org/project/sphinxawesome-sampdirective
