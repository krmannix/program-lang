---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 4 (skeleton code)
-- Tree.hs
--

-- functionName :: In_type -> Out_type
-- functionName(In_type) = Out_type

data Tree =
    Leaf
  | Twig
  | Branch Tree Tree Tree
  deriving (Eq, Show) -- 1A


twigs :: Tree -> Integer
twigs (Leaf) = 0;
twigs (Twig) = 1;
twigs (Branch b1 b2 b3) = twigs(b1) + twigs(b2) + twigs(b3)

branches :: Tree -> Integer
branches(Leaf) = 0;
branches(Twig) = 0;
branches(Branch b1 b2 b3) = 1 + branches(b1) + branches(b2) + branches(b3);

--eof