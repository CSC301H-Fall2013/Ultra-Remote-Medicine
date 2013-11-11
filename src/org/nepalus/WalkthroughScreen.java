package org.nepalus;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.media.MediaPlayer;
import android.media.MediaPlayer.OnPreparedListener;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.VideoView;

public class WalkthroughScreen extends Activity {
	Context mContext;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.walkthrough);
        mContext = this;
        
        Button nextButton = (Button) findViewById(R.id.end_walkthrough);
        nextButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
            	Intent i = new Intent(mContext, UltrasoundImageScreen.class);
            	startActivity(i);
            }
        });
        
        VideoView vv = (VideoView) findViewById(R.id.tutorial_video_view);
        vv.setOnPreparedListener (new OnPreparedListener() {                    
            @Override
            public void onPrepared(MediaPlayer mp) {
                mp.setLooping(true);
            }
        });
        
        Uri videoUri = Uri.parse("android.resource://org.nepalus/"+R.raw.tutorial);
        vv.setVideoURI(videoUri);
        vv.requestFocus();
        vv.start();
    }

}
