package gov.lanl.gmd.dbconnect;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import junit.framework.TestCase;

public class DBConnectorTest extends TestCase {
	
	public void testConnector(){
		try {
			DBConnector connector = new DBConnector();
			Connection conn = connector.getConnection();
			Statement statement = conn.createStatement();
			String querystring = "select iaga from magneto.stations";
			ResultSet r = statement.executeQuery(querystring);
			while(r.next()){
				System.out.println(r.getString("iaga"));
			}
			
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
	}
	

}
