package org.nepalus;

import java.io.IOException;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;

import android.graphics.Bitmap;

public interface NepalUltrasoundAPI {	
	String getVersion();
	
	boolean setURL(String url);
	String getURL();
	
	HttpResponse send(String personName, String comments, Bitmap image, String personAge)
		throws ClientProtocolException, IOException;
}
