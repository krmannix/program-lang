---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 4 (skeleton code)
-- Term.hs
--

data Term =
    Number Integer
  | Abs Term
  | Plus Term Term
  | Mult Term Term

evaluate :: Term -> Integer
evaluate(Number i1) = i1;
evaluate(Abs t1) = if evaluate(t1) < 0 then 0 - evaluate(t1) else evaluate(t1);
evaluate(Plus t1 t2) = evaluate(t1) + evaluate(t2);
evaluate(Mult t1 t2) = evaluate(t1) * evaluate(t2);

--eof