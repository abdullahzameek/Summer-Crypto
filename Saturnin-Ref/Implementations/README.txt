SATURNIN submission package
===========================

algorithm-specification.pdf
    Full algorithm description and specification.

cover-sheet.pdf
    Cover letter for the submission.

intellectual-property.pdf
    Intellectual property signed statements.

saturninv2.tgz
    Implementations following the NIST API.

extra/
    Extra implementations for Saturnin-Hash and Saturnin-CTR-Cascade
    with a streamable API, in C, and assembly for ARM Cortex M3 and M4.
    See extra/README.txt for details.

tests/
    Extra code for (re)generating the test vectors. These files come
    from the NIST, except genkat_aead_short.c which has been modified
    to match the input length requirements of the specialized mode
    Saturnin-Short. See tests/README.txt for details.
