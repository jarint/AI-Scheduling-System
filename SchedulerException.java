/**
 * This classes handles exceptions in the scheduler.
 * @author Jarin Thundathil
 */
public class SchedulerException extends Exception{

    /**
     * Default constructor with simple message output
     */
    public SchedulerException() {
        super("Scheduler Exception");
    }

    /**
     * Constructor calls Exception super class with message
     * @param message The message of exception
     */
    public SchedulerException(String message) {
        super(message);
    }
}
