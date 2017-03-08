package gov.lanl.gmd.dbconnect;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import junit.framework.Assert;
import junit.framework.TestCase;

public class DBConnectorTest extends TestCase {
	
	public void testConnector(){
		String[] testIDs = { // First ten ordered station IDs:
				"A01",
				"A02",
				"A03",
				"A04",
				"A05",
				"A06",
				"A07",
				"A08",
				"A09",
				"A10"};
		try {
			DBConnector connector = new DBConnector();
			Connection conn = connector.getConnection();
			Statement statement = conn.createStatement();
			String querystring = "select iaga from magneto.stations order by iaga";
			ResultSet r = statement.executeQuery(querystring);
			List<String> stationIDs = new ArrayList<>();
			while(r.next()){
				String stationID = r.getString("iaga");
				System.out.println(stationID);
				stationIDs.add(stationID);
			}
			for(int i=0;i<10;i++){
				Assert.assertTrue(testIDs[i].equals(stationIDs.get(i)));
			}
			conn.close();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
	

}
