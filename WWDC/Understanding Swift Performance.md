Hello and welcome to Understanding Swift Performance. I'm Kyle. Arnold and I are so excited to be here today to talk to you guys about Swift. 

As developers, Swift offers us a broad and powerful design space to explore. Swift has a variety of first class types and various mechanisms for code reuse and dynamism. 

All of these language features can be combined in interesting, emergent ways. So, how do we go about narrowing this design space and picking the right tool for the job? Well, first and foremost, you want to take into account the modeling implications of Swift's different abstraction mechanisms. Are value or reference semantics more appropriate? How dynamic do you need this abstraction to be? Well, Arnold and I also want to empower you today to use performance to narrow the design space. In my experience, taking performance implications into account often helps guide me to a more idiomatic solution. So, we're going to be focusing primarily on performance. We'll touch a bit on modeling. But we had some great talks last year and we have another great talk this year on powerful techniques for modeling your program in Swift. If you want to get the most out of this talk, I strongly recommend watching at least one of these talks.

All right. So, we want to use performance to narrow the design space. Well, the best way to understand the performance implications of Swift's abstraction mechanisms is to understand their underlying implementation. So, that's what we're going to do today. We're going to begin by identifying the different dimensions you want to take into account when evaluating your different abstraction mechanism options. For each of these, we're going to trace through some code using structs and classes to deepen our mental model for the overhead involved. And then we're going to look at how we can apply what we've learned to clean up and speed up some Swift code. 

In the second half of this talk, we're going to evaluate the performance of protocol oriented programming. We're going to look at the implementation of advanced Swift features like protocols and generics to get a better understanding of their modeling and performance implications. Quick disclaimer: We're going to be looking at memory representations and generated code representations of what Swift compiles and executes on your behalf. These are inevitably going to be simplifications, but Arnold and I think we've struck a really good balance between seeing simplicity and accuracy. And this is a really good mental model to reason about your code with.

All right. Let's get started by identifying the different dimensions of performance.

So, when you're building an abstraction and choosing an abstraction mechanism, you should be asking yourself, "Is my instance going to be allocated on the stack or the heap? When I pass this instance around, how much reference counting overhead am I going to incur? When I call a method on this instance, is it going to be statically or dynamically dispatched?" If we want to write fast Swift code, we're going to need to avoid paying for dynamism and runtime that we're not taking advantage of.
And we're going to need to learn when and how we can trade between these different dimensions for better performance.
All right.
 We're going to go through each of these dimensions one at a time beginning with allocation.
Swift automatically allocates and deallocates memory on your behalf.
 Some of that memory it allocates on the stack.
The stack is a really simple data structure.
 You can push onto the end of the stack and you can pop off the end of the stack.
 Because you can only ever add or remove to the end of the stack, we can implement the stack -- or implement push and pop just by keeping a pointer to the end of the stack.
 And this means, when we call into a function -- or, rather -- that pointer at the end of the stack is called the stack pointer.
 And when we call into a function, we can allocate that memory that we need just by trivially decrementing the stack pointer to make space.
 And when we've finished executing our function, we can trivially deallocate that memory just by incrementing the stack pointer back up to where it was before we called this function.
 Now, if you're not that familiar with the stack or stack pointer, what I want you to take away from this slide is just how fast stack allocation is.
 It's literally the cost of assigning an integer.
So, this is in contrast to the heap, which is more dynamic, but less efficient than the stack.
 The heap lets you do things the stack can't like allocate memory with a dynamic lifetime.
But that requires a more advanced data structure.
 So, if you're going to allocate memory on the heap, you actually have to search the heap data structure to find an unused block of the appropriate size.
 And then when you're done with it, to deallocate it, you have to reinsert that memory back into the appropriate position.
So, clearly, there's more involved here than just assigning an integer like we had with the stack.
 But these aren't even necessarily the main costs involved with heap allocation.
 Because multiple threads can be allocating memory on the heap at the same time, the heap needs to protect its integrity using locking or other synchronization mechanisms.
 This is a pretty large cost.
 If you're not paying attention today to when and where in your program you're allocating memory on the heap, just by being a little more deliberate, you can likely dramatically improve your performance.
All right.
 Let's trace through some code and see what Swift is doing on our behalf.
 Here we have a point struct with an x and y stored property.
 It also has the draw method on it.
 We're going to construct the point at (0, 0), assign point1 to point2 making a copy, and assign a value of five to point2.
x.
 Then, we're going to use our point1 and use our point2.
 So, let's trace through this.
 As we enter this function, before we even begin executing any code, we've allocated space on the stack for our point1 instance and our point2 instance.
 And because point is a struct, the x and y properties are stored in line on the stack.
 So, when we go to construct our point with an x of 0 and a y of 0, all we're doing is initializing that memory we've already allocated on the stack.
 When we assign point1 to point2, we're just making a copy of that point and initializing the point2 memory, again, that we'd already allocated on the stack.
 Note that point1 and point2 are independent instances.
 That means, when we go and assign a value of five to point2.
x, point2.
x is five, but point1.
x is still 0.
 This is known as value semantics.
 Then we'll go ahead and use point1, use point2, and we're done executing our function.
 So, we can trivially deallocate that memory for point1 and point2 just by incrementing that stack pointer back up to where we were when we entered our function.
Let's contrast this to the same exact code, but using a point which is a class instead of a struct.
All right.
 So, when we enter this function, just like before, we're allocating memory on the stack.
 But instead of for the actual storage of the properties on point, we're going to allocate memory for references to point1 and point2.
References to memory we're going to be allocated on the heap.
 So, when we construct our point at (0, 0), Swift is going to lock the heap and search that data structure for an unused block of memory of the appropriate size.
 Then, once we have it, we can initialize that memory with an x of 0, a y of 0, and we can initialize our point1 reference with the memory address to that memory on the heap.
 Note, when we allocate it on the heap, Swift actually allocated for our class point four words of storage.
 This is in contrast to the two words it allocated when our point was a struct.
 This is because now the point is a class, in addition to these stored for x and y, we're allocating two more words that Swift is going to manage on our behalf.
 Those are denoted with these blue boxes in the heap diagram.
When we assign point1 to point two, we're not going to copy the contents of point -- like we did when point1 was a struct.
 Instead, we're going to copy the reference.
 So, point1 and point2 are actually referring to the same exact instance of point on the heap.
 That means when we go and assign a value of five to point2.
x, both point1.
x and point2.
x have a value five.
 This is known as reference semantics and can lead to unintended sharing of state.
 Then, we're going to use point1, use point2, and then Swift is going to deallocate this memory on our behalf locking the heap and retraining that unused block to the appropriate position.
 And then we can pop the stack.
All right.
 So, what did we just see? We saw that classes are more expensive to construct than structs because classes require a heap allocation.
Because classes are allocated on the heap and have reference semantics, classes have some powerful characteristics like identity and indirect storage.
 But, if we don't need those characteristics for abstraction, we're going to better -- if we use a struct.
And structs aren't prone to the unintended sharing of state like classes are.
 So, let's see how we can apply that to improve the performance of some Swift code.
 Here's an example from a messaging application I've been working on.
 So, basically this is from the view layer.
 And my users send a text message and behind that text message I want to draw a pretty balloon image.
 My makeBalloon function is what generates this image and it supports a configuration of different -- or the whole configuration space of different balloons.
 For example, this balloon we see is blue color with a right orientation and a tail.
 We also support, for example, a gray balloon with a left orientation and a bubble tail.
Now, the makeBalloon function needs to be really fast because I call it frequently during allocation launch and during user scrolling.
 And so I've added this caching layer.
 So, for any given configuration, I never have to generate this balloon image more than once.
 If I've done it once, I can just get it out of the cache.
 The way I've done this is by serializing my color, orientation, and tail into a key, which is a string.
 Now, there's a couple things not to like here.
String isn't particularly a strong type for this key.
 I'm using it to represent this configuration space, but I could just as easily put the name of my dog in that key.
 So, not a lot of safety there.
 Also, String can represent so many things because it actually stores the contents of its characters indirectly on the heap.
 So, that means every time we're calling into this makeBalloon function, even if we have a cache hit, we're incurring a heap allocation.
Let's see if we can do better.
 Well, in Swift we can represent this configuration space of color, orientation, and tail just using a struct.
 This is a much safer way to represent this configuration space than a String.
 And because structs are first class types in Swift, they can be used as the key in our dictionary.
Now, when we call the makeBalloon function, if we have a cache hit, there's no allocation overhead because constructing a struct like this attributes one doesn't require any heap allocation.
 It can be allocated on the stack.
 So, this is a lot safer and it's going to be a lot faster.
Let's move on to our next dimension of performance, reference counting.
So, I glossed over a detail when we were talking about heap allocation.
 How does Swift know when it's safe to deallocate memory it allocated on the heap? Well, the answer is Swift keeps a count of the total number of references to any instance on the heap.
 And it keeps it on the instance itself.
 When you add a reference or remove a reference, that reference count is incremented or decremented.
 When that count hits zero, Swift knows no one is pointing to this instance on the heap anymore and it's safe to deallocate that memory.
The key thing to keep in mind with reference counting is this is a really frequent operation and there's actually more to it than just incrementing and decrementing an integer.
 First, there's a couple levels of indirection involved to just go and execute the increment and decrement.
 But, more importantly, just like with heap allocation, there is thread safety to take into consideration because references can be added or removed to any heap instance on multiple threads at the same time, we actually have to atomically increment and decrement the reference count.
 And because of the frequency of reference counting operations, this cost can add up.
So, let's go back to our point class and our program and look at what Swift is actually doing on our behalf.
 So, here now we have, in comparison, some generated pseudocode.
 We see our point has gained an additional property, refCount.
 And we see that Swift has added a couple calls to retain -- or a call to retain and a couple calls to release.
 Retain is going to atomically increment our reference count and release is going to atomically decrement our reference count.
 In this way Swift will be able to keep track of how many references are alive to our point on the heap.
 All right.
 And if we trace through this quickly, we can see that after constructing our point on the heap, it's initialized with a reference count of one because we have one live reference to that point.
 As we go through our program and we assign point1 to point2, we now have two references and so Swift has added a call to atomically increment the reference count of our point instance.
 As we keep executing, once we've finished using point1, Swift has added a call to atomically decrement the reference count because point1 is no longer really a living reference as far as it's concerned.
 Similarly, once we're done using point2, Swift has added another atomic decrement of the reference count.
 At this point, there's no more references that are making use of our point instance and so Swift knows it's safe to lock the heap and return that block of memory to it.
So, what about structs? Is there any reference counting involved with structs? Well, when we constructed our point struct, there was no heap allocation involved.
 When we copied, there was no heap allocation involved.
 There were no references involved in any of this.
 So, there's no reference counting overhead for our point struct.
 What about a more complicated struct, though? Here we have a label struct which contains text which is of type String and font of type UIFont.
 String, as we heard earlier, actually stores its -- the contents of its characters on the heap.
 So, that needs to be reference counted.
 And font is a class.
 And so that also needs to be reference counted.
 If we look at our memory representation, labels got two references.
 And when we make a copy of it, we're actually adding two more references, another one to the text storage and another one to the font.
 The way Swift tracks this -- these heap allocations is by adding calls to retain and release.
So, here we see the label is actually going to be incurring twice the reference counting overhead that a class would have.
 All right.
 So, in summary, because classes are allocated on the heap, Swift has to manage the lifetime of that heap allocation.
 It does so with reference counting.
 This is nontrivial because reference counting operations are relatively frequently and because of the atomicity of the reference counting.
This is just one more resent to use structs.
But if structs contain references, they're going to be paying reference counting overhead as well.
 In fact, structs are going to be paying reference counting overhead proportional to the number of references that they contain.
 So, if they have more than one reference, they're going to retain more reference counting overhead than a class.
 Let's see how we chain apply this to another example coming from my theoretical messaging application.
 So, my users weren't satisfied with just sending text messages.
 They also wanted to send attachments like images to each other.
 And so I have this struct attachment, which is a model object in my application.
 It's got a fileURL property, which stores the path of my data on disk for this attachment.
 It has a uuid, which is a unique randomly generated identifier so that we can recognize this attachment on client and server and different client devices.
 It's got a mimeType, which stores the type of data that this attachment represents like JPG or PNG or GIF.
 Probably the only nontrivial code in this example is the failable initializer, which checks if the mimeType is one of my supported mimeTypes for this application because I don't support all mimeTypes.
 And if it's not supported, we're going to abort out of this.
 Otherwise, we're going to initialize our fileURL, uuid, and mimeType.
 So, we noticed a lot of reference counting overhead and if we actually look at our memory representation of this struct, all 3 of our properties are incurring reference counting overhead when you pass them around because there are references to heap allocations underlying each of these structs.
We can do better.
First, just like we saw before, uuid is a really well defined concept.
 It's a 128 bit randomly generated identifier.
 And we don't want to just allow you to put anything in the uuid field.
 And, as a String, you really can.
 Well, Foundation this year added a new value type and so -- for uuid, which is really great because it stores those 128 bits in line directly in the struct.
 And so let's use that.
 What this is going to do is it's going to eliminate any of the reference counting overhead we're paying for that uuid field, the one that was a String.
 And we've got much more tight safety because I can't just put anything in here.
 I can only put a uuid.
 That's fantastic.
 Let's take a look at mimeType and let's look at how I've implemented this isMimeType check.
 I'm actually only supporting a closed set of mimeTypes today, JPG, PNG, GIF.
And, you know, Swift has a great abstraction mechanism for representing a fixed set of things.
 And that's an enumeration.
 So, I'm going to take that switch statement, put it inside a failable initializer and map those mimeTypes to an appropriate -- to the appropriate case in my enum.
 So, now I've got more type safety with this mimeType enum and I've also got more performance because I don't need to be storing these different cases indirectly on the heap.
 Swift actually has a really compact and convenient way for writing this exact code, which is using enum that's backed by a raw String value.
 And so this is effectively the exact same code except it's even more powerful, has the same performance characteristics, but it's way more convenient to write.
 So, if we looked at our attachment struct now, it's way more type safe.
 We've got a strongly typed uuid and mimeType field and we're not paying nearly as much reference counting overhead because uuid and mimeType don't need to be reference counted or heap allocated.
All right.
 Let's move on to our final dimension of performance, method dispatch.
When you call a method at runtime, Swift needs to execute the correct implementation.
If it can determine the implementation to execute at compile time, that's known as a static dispatch.
 And at runtime, we're just going to be able to jump directly to the correct implementation.
 And this is really cool because the compiler actually going to be able to have visibility into which implementations are going to be executed.
 And so it's going to be able to optimize this code pretty aggressively including things like inlining.
This is in contrast to a dynamic dispatch.
Dynamic dispatch isn't going -- we're not going to be able to determine a compile time directly which implementation to go to.
 And so at runtime, we're actually going to look up the implementation and then jump to it.
 So, on its own, a dynamic dispatch is not that much more expensive than a static dispatch.
 There's just one level of indirection.
 None of this thread synchronization overhead like we had with reference counting and heap allocation.
 But this dynamic dispatch blocks the visibility of the compiler and so while the compiler could do all these really cool optimizations for our static dispatches, a dynamic dispatch, the compiler is not going to be able to reason through it.
 So, I mentioned inlining.
 What is inlining? Well, let's return to our familiar struct point.
It's got an x and y and it's got a draw method.
 I've also added this drawAPoint method.
 The drawAPoint method takes in a point and just calls draw on it.
 Really fancy.
 And then the body of my program constructs a point at (0, 0) and passes that point to drawAPoint.
 Well, the drawAPoint function and the point.
draw method are both statically dispatched.
 What this means is that the compiler knows exactly which implementations are going to be executed and so it's actually going to take our drawAPoint dispatch and it's just going to replace that with the implementation of drawAPoint.
And then it's going to take our point.
draw method and, because that's a static dispatch, it can replace that with the actual implementation of point.
draw.
 So, when we go and execute this code at runtime, we're going to be able to just construct our point, run the implementation, and we're done.
 We didn't need those two -- the overhead of those two static dispatches and the associated setting up of the call stack and tearing it down.
 So, this is really cool.
 And this gets to why static dispatches and how static dispatches are faster than dynamic dispatches.
Whereas like a single static dispatch compared to a single dynamic dispatch, there isn't that much of a difference, but a whole chain of static dispatches, the compiler is going to have visibility through that whole chain.
 Whereas the chain of dynamic dispatches is going to be blocked at every single step from reasoning at a higher level without it.
 And so the compiler is going to be able to collapse a chain of static method dispatches just like into a single implementation with no call stack overhead.
 So, that's really cool.
 So, why do we have this dynamic -- this dynamic dispatch thing at all? Well, one of the reasons is it enables really powerful things like polymorphism.
 If we look at a traditional object oriented program here with a drawable abstract superclass, I could define a point subclass and a line subclass that override draw with their own custom implementation.
 And then I have a program that can polymorphically -- can create an array of drawables.
 Might contain lines.
 Might contain points.
 And it can call draw on each of them.
So, how does this work? Well, because point -- because drawable, point, and line are all classes, we can create an array of these things and they're all the same size because we're storing them by reference in the array.
 And then when we go through each of them, we're going to call draw on them.
 So, we can understand -- or hopefully we have some intuition about why the compiler can't determine at compile time which is the correct implementation to execute.
 Because this d.
draw, it could be a point, it could be a line.
 They are different code paths.
 So, how does it determine which one to call? Well, the compiler adds another field to classes which is a pointer to the type information of that class and it's stored in static memory.
 And so when we go and call draw, what the compiler actually generates on our behalf is a lookup through the type to something called the virtual method table on the type and static memory, which contains a pointer to the correct implementation to execute.
 And so if we change this d.
draw to what the compiler is doing on our behalf, we see it's actually looking up through the virtual method table to find the correct draw implementation to execute.
 And then it passes the actual instance as the implicit self-parameter.
All right.
 So, what have we seen here? Well, classes by default dynamically dispatch their methods.
 This doesn't make a big difference on its own, but when it comes to method chaining and other things, it can prevent optimizations like inlining and that can add up.
 Not all classes, though, require dynamic dispatch.
 If you never intend for a class to be subclassed, you can mark it as final to convey to your follow teammates and to your future self that that was your intention.
 The compiler will pick up on this and it's going to statically dispatch those methods.
 Furthermore, if the compiler can reason and prove that you're never going to be subclassing a class in your application, it'll opportunistically turn those dynamic dispatches into static dispatches on your behalf.
 If you want to hear about more about how this is done, check out this great talk from last year on optimizing Swift performance.
All right.
 So, where does that leave us? What I want you to take away from this first half of the talk is these questions to ask yourself.
 Whenever you're reading and writing Swift code, you should be looking at it and thinking, "Is this instance going to be allocated on the stack or the heap? When I pass this instance around, how much reference containing overhead I'm going to incur? When I call a method on this instance, is it going to be statically or dynamically dispatched?" If we're paying for dynamism we don't need, it's going to hurt our performance.
And if you're new to Swift or you're working in a code base that's been ported from objective C over to Swift, you can likely take more advantage of structs than you currently are today.
 Like we've seen with my examples here why I use structs instead of strings.
One question, though, is, "How does one go about writing polymorphic code with structs?" We haven't seen that yet.
Well, the answer is protocol oriented programming.
 And to tell you all about it, I'd like to invite Arnold up to the stage.
 Go get it.
 Thank you, Kyle.
Hello.
 I'm Arnold.
Come and join me on a journey through the implementation of protocol types and generic code starting with protocol types.
 We will look at how variables of protocol type are stored and copied and how method dispatch works.
Let's come back to our application this time implemented using protocol types.
Instead of a drawable abstract base class, we now have protocol drawable that declares the draw method.
And we have value type struct Point and struct Line conformed to the protocol.
Note, we could have also had a class SharedLine conformed to the protocol.
 However, we decided because of the unintended sharing that reference semantics that comes with classes brings with it to not to do that.
 So, let's drop it.
Our program was still polymorphic.
 We could store both values of types Point and of type Line in our array of drawable protocol type.
 However, compared to before, one thing was different.
Note that our value type struct Line and struct Point don't share a common inheritance relationship necessary to do V-Table dispatch, the mechanism that Kyle just showed us.
 So, how does Swift dispatch to the correct method? While it's going over the array in this case.
The answer to this question is a table based mechanism called the Protocol Witness Table.
There's one of those tables per type that implements the protocol in your application.
And the entries in that table link to an implementation in the type.
 OK.
 So, now we know how to find that method.
But there's still a question, "How do we get from the element in the array to the table?" And there's another question.
Note that we now have value types Line and Point.
Our Line needs four words.
Point needs two words.
 They don't have the same size.
 But our array wants to store its elements uniformly at fixed offsets in the array.
 So, how does that work? The answer to this question is that Swift uses a special storage layout called the Existential Container.
 Now, what's in there? The first three words in that existential container are reserved for the valueBuffer.
Small types like our Point, which only needs two words, fit into this valueBuffer.
Now, you might say, "Wait a second.
 What about our Line? It needs four words.
 Where do we put that?" Well, in this case Swift allocates memory on the heap and stores the value there and stores a pointer to that memory in the existential container.
Now, you saw that there was a difference between Line and Point.
 So, somehow the existential container needs to manage this difference.
 So, how does it do that? Hmmm.
 The answer to this, again, is a table based mechanism.
 In this case, we call it the Value Witness Table.
The Value Witness Table manages the lifetime of our value and there is one of those tables per type in your program.
Now, let's take a look at the lifetime of a local variable to see how this table operates.
So, at the beginning of the lifetime of our local variable of protocol type, Swift calls the allocate function inside of that table.
This function, because we now have a -- in this case -- a Line Value Witness Table, we'll allocate the memory on the heap and store a pointer to that memory inside of the valueBuffer of the existential container.
Next, Swift needs to copy the value from the source of the assignment that initializes our local variable into the existential container.
 Again, we have a Line here and so the copy entry of our value witness table will do the correct thing and copy it into the valueBuffer allocated in the heap.
OK.
 Program continues and we are at the end of the lifetime of our local variable.
 And so Swift calls the destruct entry in the value witness table, which will decrement any reference counts for values that might be contained in our type.
Line doesn't have any so nothing is necessary here.
 And then at the very end, Swift calls the deallocate function in that table.
 Again, we have a value witness table for Line so this will deallocate the memory allocated on the heap for our value.
OK.
 So, we've seen the mechanics of how Swift can generically deal with different kind of values.
 But somehow it still needs to get to those tables, right? Well, the answer is obvious.
 The next entry in the value witness table is a reference.
 In the existential container is a reference to the value witness table.
And, finally, how do we get to our protocol witness table? Well, it is, again, referenced in the existential container.
So, we've seen the mechanics of how Swift manages values of protocol type.
 Let's take a look at an example to see the existential container in action.
So, in this example we have a function that takes a protocol type parameter local and executes the draw method on it.
 And then our program creates a local variable of drawable protocol type and initializes it with a point.
And passes this local variable off to a drawACopy function call as its argument.
In order to illustrate the code that the Swift compiler generates for us, I will use Swift as a pseudocode notation underneath this example.
 And so for the existential container, I have a struct that has three words storage for valueBuffer and a reference to the value witness and protocol witness table.
 When the drawACopy function call executes, it receives the argument and passes it off to the function.
In the generated code we see that Swift passes the existential container of the argument to that function.
When the function starts executing, it creates a local variable for that parameter and assigns the argument to it.
And so in the generated code, Swift will allocate an existential container on the heap.
 Next it will read the value witness table and the protocol witness table from the argument existential container and initializes the fields in the local existential container.
 Next, it will call a value witness function to allocate a buffer if necessary and copy the value.
In this example we passed a point so no dynamic heap allocation is necessary.
This function just copies the value from the argument into the local existential container's valueBuffer.
However, had we passed a line instead, this function would allocate the buffer and copy the value there.
Next, the draw method executes and Swift looks up the protocol witness table from the field in the existential container, looks up the draw method in the fixed offset in that table and jumps to the implementation.
But wait a second.
There's another value witness call, projectBuffer.
Why is that there? Well, the draw method expects the address of our value as its input.
 And note that depending on whether our value is a small value which fits into the inline buffer, this address is the beginning of our existential container, or if we have a large value that does not fit into the inline valueBuffer, the address is the beginning of the memory allocated on the heap for us.
So, this value witness function abstracts away this difference depending on the type.
 A draw method executes, finishes, and now we are at the end of our function which means our local variable created for the parameter goes out of scope.
And so Swift calls a value witness function to destruct the value, which will decrement any reference counts if there are references in the value and deallocate a buffer if a buffer was allocated.
Our function finishes executing and our stack is removed, which removes the local existential container created on the stack for us.
OK.
 That was a lot of work.
Right? There is one thing I want you to take away from this is this work is what enables combining value types such as struct Line and struct Point together with protocols to get dynamic behavior, dynamic polymorphism.
 We can store a Line and a Point in our array of drawable protocol type.
If you need this dynamism, this is a good price to pay and compares to using classes like in the example that Kyle showed us because classes also go through a V-Table and they have the additional overhead of reference counting.
OK.
 So, we've seen how local variables are copied and how method dispatch works for values of protocol type.
 Let's look at stored properties.
So, in this example, we have a pair that contains two stored properties, first and second, of protocol -- drawable protocol type.
How does Swift store those two stored properties? Hmm.
 Well, inline of the enclosing struct.
So, if we look at -- when we allocate a pair, Swift will store the two existential containers necessary for the storage of that pair inline of the enclosing struct.
 Our program then goes and initializes this pair of the Line and the Point and so, as we've seen before, for our Line, we will allocate a buffer on the heap.
 Point fits into the inline valueBuffer and can be stored in the -- inline in the existential container.
 Now, this representation allows storing a differently typed value later in the program.
 So, the program goes and stores a Line to the second element.
 This works, but we have two heap allocations now.
OK.
 Two heap allocations.
 Well, let's look at a different program to illustrate that cost of heap allocation.
So, again, we create a Line and we create a pair and initialize this pair with the Line.
 So, we have one, two heap allocations.
 And then we create a copy of that pair again, two existential containers on the stack and then two heap allocations.
 Now, you might say, "Kyle just told us heap allocations are expensive.
 Four heap allocations? Hmm.
" Can we do anything about this? Well, remember our existential container has place for three words and references would fit into the -- into those three words because a reference is basically one word.
So, if we implemented our Line instead with a class, the -- and class is a reference semantics so they're stored by reference -- this reference would fit into the valueBuffer.
 And when we copy the first reference to the second field in our pair, only the reference is copied and we -- the only price we pay is then extra reference count increment.
Now, you might say, "Wait a second.
 Haven't we just heard about unintended sharing of state that reference semantics brings with it.
" So, if we store to the x1 field through the second field in our pair, the first field can observe the change.
And that's not what we want to have.
 We want value semantics.
 Right? Hmmm.
 What can we do about this? Well, there's a technique called copy and write that allows us to work around this.
So, before we write to our class, we check its reference count.
We've heard that when there's more than one reference outstanding to the same instants, the reference count will be greater than one, two, or three, or four, or five.
 And so if this is the case, before we write to our instance, we copy the instance and then write to that copy.
 This will decouple the state.
 OK.
 Let's take a look at how we can do this for our Line.
Instead of directly implementing the storage inside of our Line, we create a class called LineStorage that has all the fields of our Line struct.
 And then our Line struct references this storage.
And whenever we want to read a value, we just read the value inside of that storage.
However, when we come to modify, mutate our value, we first check the reference count.
 Is it greater than one? This is what the isUniquelyReferenced call here achieves.
 The only thing it does is check the reference count.
 Is it greater or equal to one? And if the reference count is greater to one -- greater than one -- we create a copy of our Line storage and mutate that.
OK.
 So, we've seen how we can combine a struct and a class to get indirect storage using copy and write.
 Let's come back to our example to see what happens here this time using indirect storage.
So, again, we create a Line.
This will create a line storage object on the heap.
 And then we use that line to initialize our pair.
 This time only the references to the line storage are copied.
When we come to copy our Line -- Again, only the references are copied and the reference count is incremented.
 This is a lot cheaper than heap allocation.
 It's a good trade off to make.
OK.
 So, we've seen how variables of protocol type are copied and stored and how method dispatch works.
 Let's take a look what that means for performance.
If we have protocol types that contain small values that can fit into the inline valueBuffer of the existential container, there is no heap allocation.
If our struct does not contain any references, there's also no reference counting.
 So, this is really fast code.
However, because of the indirection through value witness and protocol witness table, we get the full power of dynamic dispatch, which allows for dynamically polymorph behavior.
Compare this with large values.
 Large values incur heap allocations whenever we initialize or assign variables of protocol type.
 Potentially reference counting if our large value struct contain references.
However, I showed you a technique, namely using indirect storage with copy and write, that you can use to trade the expensive heap allocation.
For cheaper reference counting.
Note that this compares favorably to using classes.
 Classes also incur reference counting.
 And allocation on initialization.
 It's a good trade off to make.
 OK.
 So, we went back -- so, to summarize, protocol types provide a dynamic form of polymorphism.
 We can use value types together with protocols and can store our Lines and Points inside of an array of protocol type.
This is achieved by the use of protocol and value witness tables and existential container.
Copying of large values incurs heap allocation.
 However, I showed you a technique how you can work around this by implementing your structs with indirect storage and copy and write.
OK.
 Let's come back to our application and take a look again.
 So, in our application we had to draw a copy -- a function that took a parameter of protocol type.
However, the way that we use that is we would always use it on a concrete type.
Here we used it on a Line.
 Later in our program we would use it on a Point.
And we thought, "Hmm.
 Could we use generic code here?" Well, yes, we can.
 So, let's take a look.
 During this last part of the talk, I'll look at how variables of generic type are stored and copied and how method dispatch works with them.
 So, coming back to our application this time implemented using generic code.
 DrawACopy method now takes a generic parameter constraint to be Drawable and the rest of our program stays the same.
So, what is different when I compare this to protocol types? Generic code supports a more static form of polymorphism also known as parametric polymorphism.
 One type per call context.
What do I mean by that? Well, let's take a look at this example.
 We have the function foo, which takes a generic parameter, T constraint to be drawable, and it passes this parameter off to the function bar.
This function, again, takes a generic parameter T.
 And then our program creates a point and passes this point to the function foo.
When this function executes, Swift will bind the generic type T to the type used at this call side, which is in this case, the Point.
 When the function foo executes with this binding and it gets to the function call of bar, this -- the local variable has the type that was just found, namely Point.
 And so, again, the generic parameter T in this call context is bound through the type Point.
 As we can see, the type is substituted down the call chain along the parameters.
 This is what we mean by a more static form of polymorphism or parametric polymorphism.
 So, let's take a look of how Swift implements this under the hood.
 Again, coming back to our drawACopy function.
In this example, we pass a point.
 Like when we used protocol types, there is one shared implementation.
 And this shared implementation, if I would show you the code like I did before for protocol types, the code would look pretty similar.
 It would use protocol and value witness table to generically perform the operations inside of that function.
However, because we have one type per call context, Swift does not use an existential container here.
Instead, it can pass both the value witness table and the protocol witness table of the Point -- of the type used at this call-site as additional arguments to the function.
 So, in this case, we see that the value witness table for Point and Line is passed.
And then during execution of that function, when we create a local variable for the parameter, Swift will use the value witness table to allocate potentially any necessary buffers on the heap and execute the copy from the source of the assignment to the destination.
 And similar when it executes the draw method on the local parameter, it will use the protocol witness table passed, look up the draw method of the fixed offset in the table and jump to the implementation.
Now, I just told you there is no existential container here.
So, how does Swift allocate the memory necessary for the local parameter -- for the local variable created for this parameter? Well, it allocates a valueBuffer on the stack.
 Again, this valueBuffer is three words.
 Small values like a Point fit into the valueBuffer.
Large values like our Line are, again, stored on the heap and we store a pointer to that memory inside of the local existential container.
And all of this is managed for the use of the value witness table.
 Now, you might ask, "Is this any faster? Is this any better? Could I not -- have not just used protocol types here?" Well, this static form of polymorphism enables the compiler optimization called specialization of generics.
 Let's take a look.
So, again, here is our function drawACopy that takes a generic parameter and we pass a Point to that function call the method.
 And we have static polymorphism so there is one type at the call-site.
 Swift uses that type to substitute the generic parameter in the function and create a version of that function that is specific to that type.
So, here we have a drawACopy of a Point function now that takes a parameter that is of type Point and the code inside of that function is, again, specific to that type.
And, as Kyle showed us, this can be really fast code.
Swift will create a version per type used at a call-site in your program.
 So, if we call the drawACopy function on a Line in the Point, it will specialize and create two versions of that function.
 Now, you might say, "Wait a second.
 This has the potential to increase code size by a lot.
 Right?" But because the static typing information that is not available enables aggressive compiler optimization, Swift can actually potentially reduce the code size here.
 So, for example, it will inline the drawACopy of a Point method -- function.
 And then further optimize the code because it now has a lot more context.
 And so that function call can basically reduce to this one line and, as Kyle showed us, this can be even further reduced to the implementation of draw.
Now that the drawACopy of a Point method is no longer referenced, the compiler will also remove it and perform similar optimization for the Line example.
 So, it's not necessarily the case that this compiler optimization will increase code size.
 Can happen.
 Not necessarily the case.
OK.
 So, we've seen how specialization works, but one question to ask is, "When does it happen?" Well, let's take a look at a very small example.
 So, we define a Point and then create a local variable of that type.
 Point -- initialize it to a Point and then pass that Point as a -- for argument to the drawACopy function.
Now, in order to specialize this code, Swift needs to be able to infer the type at this call-site.
 It can do that because it can look at that local variable, walk back to its initialization, and see that it has been initialized to a Point.
Swift also needs to have the definition of both the type used during the specialization and the function -- the generic function itself available.
 Again, this is the case here.
 It's all defined in one file.
This is a place where whole module optimization can greatly improve the optimization opportunity.
Let's take a look why that is.
So, let's say I've moved the definition of my Point into a separate file.
Now, if we compile those two files separately, when I come to compile the file UsePoint, the definition of my Point is no longer available because the compiler has compiled those two files separately.
However, with whole module optimization, the compiler will compile both files together as one unit and will have insight into the definition of the Point file and optimization can take place.
Because this so greatly improves the optimization opportunity, we have now enabled a whole module optimization for default in Xcode 8.
OK.
 Let's come back to our program.
So, in our program we had this pair of Drawable protocol type.
 And, again, we noticed something about how we used it.
Whenever we wanted to create a pair, we actually wanted to create a pair of the same type, say a pair of Lines or a pair of Point.
Now, remember that the storage representation of a pair of Lines would cost two heap allocations.
When we looked at this program, we realized that we could use a generic type here.
So, if we define our pair to be generic and then the first and second property of that generic type have this generic type, then the compiler could actually enforce that we only ever create a pair of the same type.
Furthermore, we can't store a Point to a pair of Lines later in the program either.
 So, this is what we wanted, but is this -- the representation of that any better or worse for performance? Let's take a look.
So, here we have our pair.
 This time the store properties are of generic type.
Remember that I said that the type cannot change at runtime.
What that means for the generated code is that Swift can allocate the storage inline of the enclosing type.
 So, when we create a pair of Lines, the memory for the Line will actually be allocated inline of the enclosing pair.
No extra heap allocation is necessary.
 That's pretty cool.
However, as I said, you cannot store a differently typed value later to that stored property.
 But this is what we wanted.
OK.
 So, we've seen how unspecialized code works using the value witness and the protocol witness table and how the compiler can specialize code creating type-specific versions of the generic function.
Let's take a look at the performance of this first looking at specialized generic code containing structs.
 In this case, we have performance characteristics identical to using struct types because, as we just saw, the generated code is essentially as if you had written this function in terms of a struct.
 No heap allocation is necessary when we copy values of struct type around.
No reference counting if our struct didn't contain any references.
And we have static method dispatch which enables further compiler optimization and reduces your runtime -- execution time.
 Comparing this with class types, if we use class types, we get similar characteristics to classes so heap allocation and creating the instance, reference counting for passing the value around, and dynamic dispatch through the V-Table.
 Now, let's look at unspecialized generic code containing small values.
 There's no heap allocation necessary for local variables, as we've seen, because small values fit into the valueBuffer allocated in the stack.
 There's no reference counting if the value didn't contain any references.
However, we get to share one implementation across all potential call-sites through the use of the witness table -- witness tables.
OK.
 So, we've seen during this talk today how the performance characteristics of struct and classes looks like and how generic code works and how protocol types work.
What -- what can we take away from this? Oh.
 Hmm.
 There you go.
 I forgot the punchline.
 So, if we are using large values and generic code, we are incurring heap allocation.
 But I showed you that technique before, namely, using indirect storage as a workaround.
 If the large value contained references, then there's reference counting and, again, we get the power of dynamic dispatch, which means we can share one generic implementation across our code.
All right.
 So, let's come to the takeaway finally.
Choose a fitting abstraction for your -- for the entities in your application with the least dynamic runtime type requirements.
This will enable static type checking, compiler can make sure that your program is correct at compile time, and, in addition, the compiler has more information to optimize your code so you'll get faster code.
 So, if you can express the entities in your program using value types such as structs and enums, you'll get value semantics, which is great, no unintended sharing of state, and you'll get highly optimizable code.
If you need to use classes because you need, for example, an entity or you're working with an object oriented framework, Kyle showed us some techniques how to reduce the cost of reference counting.
If parts of your program can be expressed using a more static form of polymorphism, you can combine generic code with value types and, again, get really fast code, but share the implementation for that code.
 And if you need dynamic polymorphism such as in our array of drawable protocol type example, you can combine protocol types with value types and get -- get a code that is comparably fast to using classes, but you still can stay within value semantics.
 And if you run into issues with heap allocation because you're copying large values inside of protocol types or generic types, I showed you that technique, namely, using indirect storage with copy and write how to work around this.
 OK.
 So, here's some related sessions about modeling and about performance.
 And I especially want to call out the talk this afternoon about Protocol and Value Oriented Programming in your UIKit Apps.
 Thank you.
 [ Applause ]