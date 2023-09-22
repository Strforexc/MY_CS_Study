(define (over-or-under num1 num2) (cond
                                    ((> num1 num2) 1)
                                    ((< num1 num2) -1)
                                    ((= num1 num2) 0))
  )

(define (composed f g) (lambda (x) (f (g x))
                        )
)

(define (square n) (* n n))

(define (pow base exp) (cond
                         ((= exp 1) base)
                         ((= (modulo exp 2) 1)
                          (* base (square  (pow base (quotient exp 2) ))))
                         ((= (modulo exp 2) 0) (square (pow  base (quotient exp 2)) ))
                        )
)

(define (ascending? lst) (if (< (length lst) 2) #t
                           (
                             if (<= (car lst) (car (cdr lst)))
                               (ascending? (cdr lst))   #f
                            )

                          ))
