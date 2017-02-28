package gov.lanl.gmd.dbconnect;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

/**
 * A convenience class for creating a connection to the magneto database.
 *
 */
public class DBConnector {
	
	private static final String propfile = "src/main/java/gov/lanl/gmd/dbconnect/dbproperties.txt";
	private Connection connection;
	private boolean lanl = true;

	/**
	 * Constructor handles all parameters for the connection.
	 */
	public DBConnector() {
		Properties props = new Properties();
		connection = null;
		if(lanl){
			System.setProperty("http.proxyHost", "proxyout.lanl.gov");
			System.setProperty("http.proxyPort", "8080");
			System.setProperty("https.proxyHost", "proxyout.lanl.gov");
			System.setProperty("https.proxyPort", "8080");
		}
		try {
			props.load(new FileReader(propfile));
			String host = props.getProperty("host");
			String port = props.getProperty("port");
			String db = props.getProperty("db");
			String schema = props.getProperty("schema");
			String user = props.getProperty("user");
			String password = props.getProperty("password");
			String uri = "jdbc:postgresql://"+host+":"+port+"/"+db+
					"?user="+user+"&password="+password;
			connection = DriverManager.getConnection(uri);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Returns the connection to the database.
	 * @return - the connection.
	 */
	public Connection getConnection() {
		return connection;
	}
	
	
	
	

}
