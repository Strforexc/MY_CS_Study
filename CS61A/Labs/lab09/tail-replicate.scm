(define (tail-replicate x n)
  ; BEGIN
  (define (helper count lst)
    (if (= count 0)
        lst
        (helper (- count 1) (cons x lst))
      )
    )
  (helper n nil)
  ; END
)
