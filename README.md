# inductive

`inductive` is a Python library that defines inductive data structures such as Peano numbers and linked lists.

> [!CAUTION]
> It is still in early development.

## A missing puzzle piece

Despite being very useful, Python does not have a [built-in unsigned integer data type](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex). Futhermore, it does not provide the ability to refine the existing `int` type by disallowing negative numbers - at least, not in a way that static type checkers like [`mypy`](https://mypy-lang.org/) or [`pyright`](https://microsoft.github.io/pyright/) can pick up.
And yet, natural numbers come up on many occasions, such as counting or ordering, or in mundane programming tasks.

>[!TIP]
> If you have ever created your own sequence type, and defined `__len__`, you are probably aware that you get a runtime error if it returns an integer below 0.

Fortunately for us, over the years, the language's type system [has become powerful enough](https://docs.python.org/3/reference/simple_stmts.html#type) to be able to encode [inductive types](https://en.wikipedia.org/wiki/Inductive_type).

### Inductive types

The idea goes as following: you start from *something*, like a pink ball - in our case, the number 0 - to which you add a box where you can put the ball, or another box of the same kind - for natural numbers, this is the [successor function](https://en.wikipedia.org/wiki/Successor_function). Then, you put the ball in a box, which itself is inside another box, and so on: you now have a number. What is its value? Simply count how many boxes you need to open to get to the ball.

![A pink ball surrounded by three boxes. The whole setup corresponds to the number 3.](./assets/boxes_and_balls_nat.png)

> Temporary mouse-drawn thingy until I find a better analogy 😆

Another way to think of it (and maybe even a better one!) is through [recursive functions](https://en.wikipedia.org/wiki/Recursion_(computer_science)), except that instead of returning values, it creates inhabitants of the type in a way that can understood statically.

## What does it give us?

This way, we are able to represent natural numbers in a type-safe way! If a value is of type `Nat`, you know it cannot be negative, which is sometimes a nice guarantee to have [as aforementioned](#a-missing-puzzle-piece). Also, this is very similar to the [Peano axioms](https://en.wikipedia.org/wiki/Peano_axioms), which gives us very nice mathematical properties.

However, this does not come without sacrificing some practicality: there is, as of writing this, no way to make the numeric literals have the type `Nat` instead of the built-in `int`. We still enjoy operators such as `+` or `*` thanks to their [corresponding magic methods](https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types), but we will have to use functions to convert literals to our natural number type.

## But why stop here?

...We don't!

With the `type` statement added in Python 3.12 and structural pattern matching with `match`/`case` in 3.10, the language unlocked a lot of power at the type level. The latter, especially, is the best friend of inductive types ; and `Nat` is not the only one that is very useful!

Especially, I'm looking forward adding linked lists, inductive sets, trees, other numeric types that fit very well this little world.

>[!IMPORTANT]
> For now, only `Nat` is implemented, but it's just a matter of time before the others get added too 😄

`inductive` also provides a submodule `builtins` which goal is to override existing built-ins to use better suited types: for example, `len` is replaced by `length`, which returns a `Nat`, more appropriated since `len` can never return a negative number.

## Where does this idea come from?

More specifically, this library is heavily inspired by the proof assistant [Rocq](https://en.wikipedia.org/wiki/Coq_(software)) (previously known as Coq) and its programming language Gallina, which are based on a type theory called [calculus of constructions](https://en.wikipedia.org/wiki/Calculus_of_constructions), and more recently on its variant called [PCUIC](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.FSCD.2018.29) (predicative calculus of cumulative inductive constructions).
