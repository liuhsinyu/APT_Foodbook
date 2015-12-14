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
import android.widget.GridView;
import android.os.StrictMode;

import com.facebook.CallbackManager;
import com.facebook.GraphRequest;
import com.facebook.AccessToken;
import com.facebook.HttpMethod;
import com.facebook.GraphResponse;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.nio.Buffer;
import java.util.ArrayList;

public class RecipeBoxFragment extends Fragment {
    final ArrayList<String> user_id = new ArrayList<String>();
    final ArrayList<String> recipeIds = new ArrayList<String>();
    final ArrayList<String> recipeNames = new ArrayList<String>();
    final ArrayList<String> recipePhotos = new ArrayList<String>();
    final ArrayList<String> recipeTags = new ArrayList<String>();

    public static RecipeBoxFragment newInstance(int recipe_type) {
        RecipeBoxFragment myFragment = new RecipeBoxFragment();

        Bundle args = new Bundle();
        args.putInt("type", recipe_type);
        myFragment.setArguments(args);

        return myFragment;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, final ViewGroup container,
                             Bundle savedInstanceState) {
        final View view = inflater.inflate(R.layout.activity_recipebox, container, false);
        int type = getArguments().getInt("type");
        System.out.println(type);
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        GraphRequest request = new GraphRequest(
                AccessToken.getCurrentAccessToken(),
                "/me",
                null,
                HttpMethod.GET,
                new GraphRequest.Callback() {
                    public void onCompleted(GraphResponse response) {
                        try {
                            System.out.println(response.toString());
                            JSONObject obj = response.getJSONObject();
                            user_id.clear();
                            user_id.add(obj.getString("id"));
                        } catch(JSONException ex) {
                            ex.printStackTrace();
                        }
                    }
                }
        );
        request.executeAndWait();
        final String request_url = "http://foodbook-1150.appspot.com/recipebox_json?list_type="+type+"&user_id="+user_id.get(0);
        System.out.println(request_url);
        try {
            URL obj = new URL(request_url);
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();

            // optional default is GET
            con.setRequestMethod("GET");

            int responseCode = con.getResponseCode();

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
            System.out.println(response.toString());
            recipeIds.clear();
            recipeNames.clear();
            recipePhotos.clear();
            recipeTags.clear();
            JSONObject jObject = new JSONObject(response.toString());
            JSONArray ids = jObject.getJSONArray("id");
            JSONArray names = jObject.getJSONArray("name");
            JSONArray photos = jObject.getJSONArray("photo");
            JSONArray tags = jObject.getJSONArray("tags");

            for (int i = 0; i < ids.length(); i++) {
                System.out.println(ids.getString(i));
                recipeIds.add(ids.getString(i));
                recipeNames.add(names.getString(i));
                recipePhotos.add(photos.getString(i));
                JSONArray tag = tags.getJSONArray(i);
                String tag_str = "";
                for(int j =0;j<tag.length();j++) {
                    System.out.println(tag.getString(j));
                    tag_str+="#"+tag.getString(j);
                }
                System.out.println(tag_str);
                recipeTags.add(tag_str);
            }
        }catch (Exception e){

        }

        GridViewScrollable gridview = (GridViewScrollable) view.findViewById(R.id.gridview);
        gridview.setAdapter(new ImageTxtAdapter(container.getContext(),getActivity(), recipeIds, recipePhotos, recipeNames,recipeTags));
        return view;
    }

}
