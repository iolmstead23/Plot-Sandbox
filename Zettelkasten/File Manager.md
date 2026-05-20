File managers are able to bundle files into directories or folders. Directories can be placed within other directories, resulting in a hierarchical file structure. The directory path tells a user where the file is located within the file system. Directory paths are often written as the folder names separated by slashes. For example, a job seeker saves their files in the [[Linux]] environment as /home/mei/JobSearch/MyResumes/MyCoverLetters. The figure below is a depiction of a [[Linux]] file structure.

There are some key differences in working with [[Windows]] and [[Linux]] file structures. In a [[Windows]] shell

- a backward slash (\) is used to express directory paths;
- [[Windows]] is not case sensitive when searching for files, which means capitalization is irrelevant;
- [[Windows]] root directory is referred to by letter, commonly C drive; and
- the user’s home directory is found within C:\Users.

In a [[Linux]] shell

- a forward slash (/) is used to express directory paths;
- [[Linux]] is case-sensitive;
- the root directory in [[Linux]] is expressed as a single forward slash; and
- most flavors of [[Linux]] place the home directory within the /home/.

Consider how you organize your [[computer]] files.
### Memory Management

The memory manager is another component of an [[Operating System|operating system]]’s [[Kernel|kernel]]. The memory manager manages the system’s primary main memory. When a [[computer]] is performing a single task, managing the memory is minimal. When a [[computer]] is performing many tasks simultaneously, the duties of the memory manager are extensive. The memory manager needs to find and assign the main memory space for each of the processes and restrict the actions of each process to the memory space allocated to that program. When more main memory space is needed, the memory manager can create an illusion of additional space by rotating programs and [[data]] between the primary and secondary memory, a technique called paging. The additional memory space created in secondary memory by paging is referred to as virtual memory.