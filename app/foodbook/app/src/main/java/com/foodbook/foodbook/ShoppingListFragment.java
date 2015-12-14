package com.foodbook.foodbook;

import android.os.Bundle;
import android.os.StrictMode;
import android.content.Intent;
import android.support.v4.app.Fragment;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Button;
import android.widget.Toast;

import com.facebook.AccessToken;
import com.facebook.GraphRequest;
import com.facebook.GraphResponse;
import com.facebook.HttpMethod;

import org.apache.http.Header;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.client.HttpClient;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.ByteArrayInputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;

import com.beardedhen.androidbootstrap.BootstrapButton;
import com.beardedhen.androidbootstrap.BootstrapEditText;
import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;

/**
 * Created by liuhsinyu on 15/12/12.
 */
public class ShoppingListFragment extends Fragment {
    final ArrayList<String> user_id = new ArrayList<String>();
    final ArrayList<Product> items = new ArrayList<Product>();
    ItemAdapter mProductAdapter = null;

    @Override
    public View onCreateView(LayoutInflater inflater, final ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.activity_shoppinglist, container, false);

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

        final String request_url = "http://foodbook-1150.appspot.com/shoppingpage_json?user_id="+user_id.get(0);
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
            items.clear();
            JSONObject jObject = new JSONObject(response.toString());
            JSONArray res_items = jObject.getJSONArray("item");

            for (int i = 0; i < res_items.length(); i++) {
                items.add(new Product(res_items.getString(i)));
            }
        }catch (Exception e){

        }
        ListView listViewCatalog = (ListView) view.findViewById(R.id.shoppinglist);
        mProductAdapter = new ItemAdapter(container.getContext(),items);
        listViewCatalog.setAdapter(mProductAdapter);

        listViewCatalog.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Product selectedProduct = items.get(position);
                System.out.println(position);
                if (selectedProduct.selected == true) {
                    System.out.println("true");
                    selectedProduct.selected = false;
                } else {
                    System.out.println("false");
                    selectedProduct.selected = true;
                }
                for (int i = items.size() - 1; i >= 0; i--) {
                    if (items.get(i).selected) {
                        System.out.println(i);
                    }
                }
                mProductAdapter.notifyDataSetInvalidated();
            }
        });
        final ArrayList<String> idx_list = new ArrayList<String>();
        BootstrapButton removeButton = (BootstrapButton)view.findViewById(R.id.ButtonRemoveFromCart);
        removeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                idx_list.clear();
                for (int i = items.size() - 1; i >= 0; i--) {
                    if (items.get(i).selected) {
                        idx_list.add("" + i);
                    }
                }
                String remove_str = "";
                for (int i = 0; i < idx_list.size(); i++) {
                    if (i == idx_list.size() - 1)
                        remove_str += idx_list.get(i);
                    else
                        remove_str += idx_list.get(i) + ",";
                }

                System.out.println(remove_str);
                /*
                final String request_url2 = "http://foodbook-1150.appspot.com/shoppingpage_delete";
                try {
                    HttpClient httpClient = new DefaultHttpClient();
                    HttpPost httpPost = new HttpPost(request_url2);

                    ArrayList<NameValuePair> params = new ArrayList<NameValuePair>();
                    params.add(new BasicNameValuePair("user_id", user_id.get(0)));
                    params.add(new BasicNameValuePair("DeleteItem", remove_str));
                    httpPost.setEntity(new UrlEncodedFormEntity(params));
                    HttpResponse response = httpClient.execute(httpPost);

                } catch (Exception e) {

                }*/

                final String request_url2 = "http://foodbook-1150.appspot.com/shoppingpage_delete";
                RequestParams params = new RequestParams();
                params.put("user_id", user_id.get(0));
                params.put("DeleteItem", remove_str);

                AsyncHttpClient client = new AsyncHttpClient();
                client.post(request_url2, params, new AsyncHttpResponseHandler() {
                    @Override
                    public void onSuccess(int statusCode, Header[] headers, byte[] response) {
                        Toast.makeText(container.getContext(), "Remove Successful", Toast.LENGTH_SHORT).show();
                        ((MainActivity) getActivity()).displayView(R.id.nav_shopping_list);
                    }

                    @Override
                    public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e) {
                        System.out.println(e.toString());
                    }

                });
                ((MainActivity) getActivity()).displayView(R.id.nav_shopping_list);

            }
        });

        final BootstrapEditText newItemText = (BootstrapEditText)view.findViewById(R.id.new_item);
        final BootstrapButton addButton = (BootstrapButton)view.findViewById(R.id.add_item);

        newItemText.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                if(!newItemText.getText().equals(""))
                    addButton.setEnabled(true);
                else
                    addButton.setEnabled(false);
            }
        });

        addButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final String request_url2 = "http://foodbook-1150.appspot.com/shoppingpage_add";
                try {
                    HttpClient httpClient = new DefaultHttpClient();
                    HttpPost httpPost = new HttpPost(request_url2);

                    ArrayList<NameValuePair> params = new ArrayList<NameValuePair>();
                    params.add(new BasicNameValuePair("user_id", user_id.get(0)));
                    params.add(new BasicNameValuePair("newItem", newItemText.getText().toString()));
                    httpPost.setEntity(new UrlEncodedFormEntity(params));
                    HttpResponse response = httpClient.execute(httpPost);

                } catch (Exception e) {

                }

                ((MainActivity) getActivity()).displayView(R.id.nav_shopping_list);
            }
        });

        return view;
    }
}
