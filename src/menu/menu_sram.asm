.segment "menu_code"

; ------------------------------------------------------------------------------

; [ check if sram is valid ]
; [ sram expansion ]

CheckSRAM:
@7023:  longa
        lda     #$e41b                  ; fixed value
        cmp     $337f08                 ; $307ff8 before
        beq     @7047
        cmp     $337f0a                 ; $307ffa before
        beq     @7047
        cmp     $337f0c                 ; $307ffc before
        beq     @7047
        cmp     $337f0e                 ; $307ffe before
        beq     @7047
        shorta
        jsr     ClearSRAM
        clc
        rts
@7047:  shorta
        sec
        rts

; ------------------------------------------------------------------------------

; [ clear sram ]
; [ sram expansion ]

ClearSRAM:
@704b:  longa
        clr_ax
@loop:  sta     $306000,x
        sta     $316000,x
        sta     $326000,x
;        sta    $336000,x
        inx2
        cpx #$2000
        bne @loop
        shorta
        rts

; ------------------------------------------------------------------------------

; [ reset saved menu cursor positions ]

ResetMenuCursorMemory:
@7068:  ldx     #0
@706b:  stz     $022b,x                 ; clear saved menu cursor positions
        inx
        cpx     #$001f
        bne     @706b
        lda     #$01                    ; character skills cursors default to magic
        sta     $0237
        sta     $0239
        sta     $023b
        sta     $023d
        rts

; ------------------------------------------------------------------------------

; [ make sram valid ]
; [ sram expansion ]

ValidateSRAM:
@7083:  longa
        lda     #$e41b                  ; set fixed value
        sta     $337f08
        sta     $337f0a
        sta     $337f0c
        sta     $337f0e
        shorta
        rts

; ------------------------------------------------------------------------------

; [ init saved game data ]

InitSaveSlot:
@709b:  jsr     ResetMenuCursorMemory
        ldy     #$7fff                  ; set default font color
        sty     $1d55
        lda     #$12                    ; set default button mappings
        sta     $1d50
        lda     #$34
        sta     $1d51
        lda     #$56
        sta     $1d52
        lda     #$06
        sta     $1d53
        lda     #$2a                    ;
        sta     $1d4d
        clr_ay
        sty     $1dc7                   ;
        stz     $1d54
        stz     $1d4e
        stz     $1d4f
        sty     $1863                   ; clear game time
        stz     $1865
        sty     $1860                   ; clear gp
        stz     $1862
        sty     $1866                   ; clear steps
        stz     $1868
        sty     $021b                   ; clear menu game time
        sty     $021d
        jsr     InitWindowPal
        rts

; ------------------------------------------------------------------------------
