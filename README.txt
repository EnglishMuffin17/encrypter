KnitCryption Documentation and how-to

KnitCryption/KnitCrypter is intended to make encrypting files/strings/data
simpler and less of a hassle. Still a constant work in progress, It's not the
end of the world is something is 'missing' from the overall project.

There are some basics to go over first, these are the main tools KnitCrypter has
to offer.

knitpattern; a knitpattern object accepts a minimum of two arguments but has the
following available:

    1. string; a string of unique characters which will be refrenced for 
    assignment. It is recommended to utilize the string library to produce all
    available characters. This is done so that the user can define thier own
    sequence.

    2. base; this is the base type a knitpattern object will utilize to generate
    numerical assignment values. At this current time, it only accepts 2-10 or
    hex and oct as appropriate base types, but RND is looking into expanding the
    functionality.

    3. func; by default, there is a function already in place that just returns
    the current value of iteration, but is left as a keyword that the user may
    implement thier own values to assignment. e.g. 'lambda x,y: x**y' where 'x'
    is already defined by the generator and any 'args' passed into the
    knitpattern object will be passed into the following arguments of the 
    function.

If a sequence does not return with any equivalent, a successful knitpattern
object will be created! Congrats! After a new object is created, it will have
the following attributes available:

    1. prefix; the prefix property will return the base type of the object in
    string form. e.g. 'hex' returns '0x' or 'base 6' returns '6b'.

    2. sequence; the sequence property returns a dict object after calling a 
    sub-property of either 'from_keys' or 'from_values'. 'from_keys' returns 
    the original dictionary where the keys are-- go figure --the keys of the
    new dictionary object, 'from_values' being the inverse and returning a dict
    object where the values are the head of the new dict object.

knitpattern objects allow the user to get thier total length directly from 
calling 'len(knitpattern)' but is not immediately iterable. Instead use the
sequence property to iterate through a knitpattern object.