module Typecheck where

import AbstractSyntax
import Parse

class Typeable a where
  chk :: [(String, Type)] -> a -> Maybe Type
  
instance Typeable Exp where 
  chk env (And e1 e2) = let p1 = chk env e1
  						let p2 = chk env e2
  						if p1 == p2 then Just Bool else Nothing
  chk env (Or  e1 e2) = let p1 = chk env e1
  						let p2 = chk env e2
  						if p1 == p2 then Just Bool else Nothing
  chk env (Not e1   ) = let p1 = chk env e1
  						if typeOf p1 == Just Bool then Just Bool else Nothing
  chk env      e1     = if e1 == "true" || e1 == "false" 
  							then Just Bool 
  							else 
  								let f = [ t | (s, t) <- env, s == e1]
  								if length f > 0 then head f else Nothing
  chk _ _ = Nothing -- Implement for Problem #1, part (c).

instance Typeable Stmt where 
  chk env (Assign x e s) = Just Void
  chk env (Print    e s) = if typeOf (chk env e) == Just Bool && typeOf (chk env s) == Just Void then Just Void else Nothing
  chk env (End        _) = Just Void
  chk _ _ = Nothing -- Implement for Problem #1, part (c).

-- eof