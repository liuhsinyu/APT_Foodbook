package com.foodbook.foodbook;

import android.content.Context;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.view.View;
import android.content.Intent;
import android.util.Log;
import android.widget.Toast;
import android.support.v7.widget.Toolbar;
import android.widget.TextView;

import com.facebook.CallbackManager;
import com.facebook.FacebookCallback;
import com.facebook.FacebookException;
import com.facebook.FacebookSdk;
import com.facebook.GraphRequest;
import com.facebook.GraphResponse;
import com.facebook.login.LoginResult;
import com.facebook.login.widget.LoginButton;
import com.facebook.AccessTokenTracker;
import com.facebook.AccessToken;
import com.facebook.login.widget.ProfilePictureView;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.Arrays;
import java.util.List;

public class HomeFragment extends Fragment {
    private LoginButton loginButton;
    private AccessTokenTracker fbTracker;
    private CallbackManager callbackManager;

    @Override
    public View onCreateView(LayoutInflater inflater, final ViewGroup container,
                         Bundle savedInstanceState) {
        FacebookSdk.sdkInitialize(container.getContext());
        final View view = inflater.inflate(R.layout.activity_home, container, false);
        callbackManager = CallbackManager.Factory.create();
        loginButton = (LoginButton) view.findViewById(R.id.login_button);
        loginButton.setFragment(this);
//        loginButton.setVisibility(View.INVISIBLE);
        List<String> permissionNeeds = Arrays.asList("user_photos", "email", "user_birthday", "public_profile");
        loginButton.setReadPermissions(permissionNeeds);
        // Initialize the SDK before executing any other operations,
        // especially, if you're using Facebook UI elements.
        loginButton.registerCallback(callbackManager, new FacebookCallback<LoginResult>() {
            @Override
            public void onSuccess(LoginResult loginResult) {
                System.out.println("onSuccess");
                GraphRequest request = GraphRequest.newMeRequest(loginResult.getAccessToken(),
                        new GraphRequest.GraphJSONObjectCallback() {
                            @Override
                            public void onCompleted(JSONObject object, GraphResponse response) {
                                try {
                                    Toast.makeText(container.getContext(),"Successfully Login with Facebook",Toast.LENGTH_SHORT).show();

                                    TextView t_welcome = (TextView)view.findViewById(R.id.welcome);
                                    t_welcome.setText("Successfully logging in, " + object.getString("name") + "!\nStart exploring Foodbook!");

                                    TextView t_name = (TextView)container.getRootView().findViewById(R.id.user_name);
                                    t_name.setText(object.getString("name"));

                                    TextView t_mail = (TextView)container.getRootView().findViewById(R.id.user_email);
                                    t_mail.setText(object.getString("email"));

                                    ProfilePictureView profilePictureView = (ProfilePictureView)container.getRootView().findViewById(R.id.user_profile);
                                    profilePictureView.setProfileId(object.getString("id"));
                                    profilePictureView.setPresetSize(ProfilePictureView.SMALL);
                                    ((AppCompatActivity)getActivity()).getSupportActionBar().show();

                                    System.out.println(object.toString());
                                    System.out.println("Hi, " + object.getString("birthday"));

                                } catch (JSONException ex) {
                                    ex.printStackTrace();
                                }
                            }
                        });
                Bundle parameters = new Bundle();
                parameters.putString("fields", "id,name,email,gender, birthday");
                request.setParameters(parameters);
                request.executeAsync();


            }

            @Override
            public void onCancel() {
                System.out.println("onCancel");
                Toast.makeText(container.getContext(),"Successfully Logout with Facebook",Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onError(FacebookException exception) {
                System.out.println("onError");
                Log.v("LoginActivity", exception.getCause().toString());
            }
        });
        fbTracker = new AccessTokenTracker() {
            @Override
            protected void onCurrentAccessTokenChanged(AccessToken accessToken, AccessToken accessToken2) {
                if (accessToken2 == null) {
                    Toast.makeText(container.getContext(), "Successfully Logout with Facebook", Toast.LENGTH_SHORT).show();
                    ((AppCompatActivity)getActivity()).getSupportActionBar().hide();
                }
            }
        };
        return view;
    }


    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        callbackManager.onActivityResult(requestCode, resultCode, data);
    }

}
