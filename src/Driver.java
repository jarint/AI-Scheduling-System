package src;

/**
 * src.Driver class run the program
 */
public class Driver {

    public static void main(String[] args) throws SchedulerException{
        Scheduler s = new Scheduler();
        s.start(args);
    }
}
