Multi-core CPU benchmark that does integer math and outputs a score out of 1000 based on the performance of your CPU. My i9-9900K scores 239/1000. I have NOT tested with other systems, so I don't know how accurate it is. Credit goes to ChatGPT for the code, but it will need a lot of manual improvements.

BUGS (that ChatGPT was unable to fix):

* Sometimes the app will lock at the end of the test.
* The CPU model does not output the CPU in the form I'd like it to
* The mean CPU speed counter is not accurate at all. I'd like this to calculate the average CPU speed during the tests, considering Intel Turbo Boost usually boosts the clock speed during intensive tasks.
* I don't know how accurate the CPU scoring is. I only tested this on my system (running an i9-9900K).

Screenshot:

![image](https://github.com/user-attachments/assets/7b8aa845-845d-41e6-9553-fc907f02c9e6)
