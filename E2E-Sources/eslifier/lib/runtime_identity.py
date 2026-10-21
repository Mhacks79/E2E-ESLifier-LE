"""The one runtime DLL this tool installs against, by SHA-256.

Update RUNTIME_SHA whenever a new LELightSupport.dll is built for delivery and move
the previous value into LEGACY_RUNTIME_SHA, so an installed older copy is still
recognised during a scan (it is never accepted for installation).
"""
RUNTIME_SHA='8163276742248b229889ff071bf02c9d51cdb51e0812b0aebec313352b86a04e'
LEGACY_RUNTIME_SHA={
    'd5f15e5446e09a4704cf77c79d0c420b0d60ceb01d802cd2f8ec731f7b03ee19', # runtime12 named-query overhead correction
    '18d2096f0731a0192989644ab78d6f7bd0acba8406f746e04ebbc7fec18fe640', # runtime11 integrated string32 protection
    '1c2d081ae337a2ce0e1c2c4550966082cd00fcc479707e37e2757690fe182d13', # runtime10 dialogue-branch correction
    '956bc3c0becfcd5a768d302f4783a21c8a1858d9d5f8b0f0d146504eceef2462', # runtime9 caller/classification diagnostic
    'b3b2a36e1121726c910d20556870533004888221a33ec3f55d79457ecd3024ad', # runtime8 light self-fallback correction
    '39f3853b6bd80153ba45cd9c5f222810b83cdfc5fd2fa0e5b2d2d06e26f9358f',  # runtime7 capacity diagnostic

    'bf51c50e6e86a433d6924f25fd6a9edad7b08bd00e725ce392c8924099dbfc3e',  # runtime6, ambiguous capacity diagnostic

    '3d5c3b4bf02f923b915b7c890c4e8ce8acaa73511e80f30960a84ef240579f44',  # 2026-10-19 first release: stopped at Skyrim.esm header
    'b673904ed2c86679f4bb6f06740b9aa8035b5ab51a7da2c40a18eca552c3d0e4',  # 2026-10-17 test candidate
    '00f7ec6ceb32edb60cc94616751b0df0a30a416a6805145590a88766266324dd',  # 0.5
    '78ae13813b754ad970ad8fe8ce9dedffe160a639f8cfbbf2978275c44b4aea19',
    '1037826473aa309132bcf9c4f9598830dc79902dfa02b99d6162bb774c51b1c5',
}
KNOWN_RUNTIME_SHA={RUNTIME_SHA}|LEGACY_RUNTIME_SHA
