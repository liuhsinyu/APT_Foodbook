package com.foodbook.foodbook;

import android.os.StrictMode;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ExpandableListView;
import android.widget.ImageView;
import android.view.MotionEvent;

import com.beardedhen.androidbootstrap.AwesomeTextView;
import com.beardedhen.androidbootstrap.BootstrapButton;
import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * Created by liuhsinyu on 15/12/13.
 */
public class ViewRecipeFragment extends Fragment{
    List<String> parentHeaderInformation;

    public static ViewRecipeFragment newInstance(String recipe_id) {
        ViewRecipeFragment myFragment = new ViewRecipeFragment();

        Bundle args = new Bundle();
        args.putString("recipe_id", recipe_id);
        myFragment.setArguments(args);

        return myFragment;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, final ViewGroup container,
                             Bundle savedInstanceState) {
        final View view = inflater.inflate(R.layout.activity_viewrecipe, container, false);
        final String recipe_id = getArguments().getString("recipe_id");
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        System.out.println("VIEW RECIPE ID");
        System.out.println(recipe_id);

        final List<String> infos = new ArrayList<String>();
        List<String> ingredients = new ArrayList<String>();
        List<String> directions = new ArrayList<String>();
        List<String> comments = new ArrayList<String>();


        final String request_url = "http://foodbook-1150.appspot.com/viewpage_json?recipe_id="+recipe_id;
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
            ingredients.clear();
            directions.clear();
            comments.clear();
            JSONObject jObject = new JSONObject(response.toString());
            System.out.println(jObject.getString("author"));
            infos.add(jObject.getString("author"));
            infos.add(jObject.getString("recipe_name"));
            infos.add(jObject.getString("estimate_time"));
            infos.add(jObject.getString("photo_urls"));
            infos.add(Integer.toString(jObject.getInt("portion")));
            JSONArray ingredients_arr = jObject.getJSONArray("ingredients");
            JSONArray directions_arr = jObject.getJSONArray("directions");
            JSONArray comments_arr = jObject.getJSONArray("comments_list");
            for (int i = 0; i < ingredients_arr.length(); i++)
                ingredients.add(ingredients_arr.getString(i));

            for (int i = 0; i < directions_arr.length(); i++)
                directions.add(directions_arr.getString(i));

            for (int i = 0;i<comments_arr.length();i++){
                comments.add(comments_arr.getJSONObject(i).getString("author")+" : "+comments_arr.getJSONObject(i).getString("comment_text"));
            }

        }catch (Exception e){

        }


        AwesomeTextView recipe_name = (AwesomeTextView) view.findViewById(R.id.recipe_name);
        AwesomeTextView recipe_author = (AwesomeTextView) view.findViewById(R.id.recipe_author);
        ImageView recipe_photo = (ImageView) view.findViewById(R.id.recipe_photo);
        AwesomeTextView recipe_time = (AwesomeTextView) view.findViewById(R.id.recipe_time);
        AwesomeTextView recipe_portion = (AwesomeTextView) view.findViewById(R.id.recipe_portion);

        parentHeaderInformation = new ArrayList<String>();
        parentHeaderInformation.add("Ingredients");
        parentHeaderInformation.add("Directions");
        parentHeaderInformation.add("Comments");
        HashMap<String, List<String>> allChildItems = new HashMap<String, List<String>>();
        allChildItems.put(parentHeaderInformation.get(0), ingredients);
        allChildItems.put(parentHeaderInformation.get(1), directions);
        allChildItems.put(parentHeaderInformation.get(2), comments);

        ExpandableListView recipe_options = (ExpandableListView) view.findViewById(R.id.expandableListView);
        ExpandableListAdapter listAdapter = new ExpandableListAdapter(container.getContext(),parentHeaderInformation, allChildItems);
        recipe_options.setAdapter(listAdapter);

        recipe_options.setOnTouchListener(new ExpandableListView.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                int action = event.getAction();
                switch (action) {
                    case MotionEvent.ACTION_DOWN:
                        // Disallow ScrollView to intercept touch events.
                        v.getParent().requestDisallowInterceptTouchEvent(true);
                        break;

                    case MotionEvent.ACTION_UP:
                        // Allow ScrollView to intercept touch events.
                        v.getParent().requestDisallowInterceptTouchEvent(false);
                        break;
                }

                // Handle ListView touch events.
                v.onTouchEvent(event);
                return true;
            }
        });
        recipe_author.setText("by " + infos.get(0));
        recipe_name.setText(infos.get(1));
        recipe_photo.setScaleType(ImageView.ScaleType.CENTER_CROP);
        recipe_time.setText(infos.get(2));
        Picasso.with(container.getContext()).load(infos.get(3)).into(recipe_photo);
        recipe_portion.setText(infos.get(4));

        BootstrapButton imadeitButton = (BootstrapButton)view.findViewById(R.id.ButtonIMadeIt);
        imadeitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v){
                ((MainActivity)getActivity()).displayIMadeItView(recipe_id,infos.get(1));
            }
        });
        return view;
    }

}
