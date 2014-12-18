module TypeCheck where

import AbstractSyntax
import Parse

class Typeable a where
  chk :: [(String, Type)] -> a -> Maybe Type
  
instance Typeable Exp where 
  chk env (And e1 e2) = let Just p1 = chk env e1
                            Just p2 = chk env e2
  						in if p1 == Bool && p2 == Bool then Just Bool else Nothing
  chk env (Or  e1 e2) = let Just p1 = chk env e1
                            Just p2 = chk env e2
                        in if p1 == Bool || p2 == Bool then Just Bool else Nothing
  chk env (Not e1   ) = let p1 = chk env e1
  						in if p1 == Just Bool then Just Bool else Nothing
  chk env (Variable v) =
  								let f = [ t | (s, t) <- env, s == v]
                  in if null f
                    then Nothing
                  else
                    Just Bool 
  chk env (Value x) = Just Bool

instance Typeable Stmt where 
  chk env (Assign x e s) = Just Void
  chk env (Print    e s) = if chk env e == Just Bool && chk env s == Just Void then Just Void else Nothing
  chk env  End           = Just Void

-- eof