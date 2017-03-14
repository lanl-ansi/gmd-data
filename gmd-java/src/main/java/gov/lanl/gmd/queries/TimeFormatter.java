package gov.lanl.gmd.queries;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Date;

public class TimeFormatter {
	
	public static String formatTimestamp(Timestamp timestamp){
		Date date = new Date();
		date.setTime(timestamp.getTime());
		return new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(date);
	}

}
