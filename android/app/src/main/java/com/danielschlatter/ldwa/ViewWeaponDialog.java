package com.danielschlatter.ldwa;

import android.app.AlertDialog;
import android.app.Dialog;
import android.database.Cursor;
import android.graphics.drawable.Drawable;
import android.nfc.Tag;
import android.os.Bundle;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.content.res.ResourcesCompat;
import androidx.fragment.app.DialogFragment;

public class ViewWeaponDialog extends DialogFragment {
    private Weapon weapon;
    private final DataAdapter dataAdapter;
    public ViewWeaponDialog(DataAdapter dataAdapter) {this.dataAdapter = dataAdapter;}
    @NonNull
    @Override
    public Dialog onCreateDialog(@Nullable Bundle savedInstanceState) {
        Dialog dialog = super.onCreateDialog(savedInstanceState);
        dialog.setCanceledOnTouchOutside(true);
        LayoutInflater inflater = requireActivity().getLayoutInflater();
        View title = inflater.inflate(R.layout.title_bar, null);
        TextView name = title.findViewById(R.id.name);
        name.setText(weapon.getName());
        TextView type = title.findViewById(R.id.type);
        TextView archetype = title.findViewById(R.id.archetype);
        ImageView icon = title.findViewById(R.id.icon);
        ImageView ammo_icon = title.findViewById(R.id.ammo);
        ImageView element_icon = title.findViewById(R.id.element);
        type.setText(weapon.getType());
        archetype.setText(weapon.getArchetype());
        icon.setImageResource(this.requireContext().getResources().getIdentifier(weapon.getIcon(), "mipmap", this.requireContext().getPackageName()));
        element_icon.setImageResource(this.requireContext().getResources().getIdentifier(weapon.getElement_icon(), "mipmap", this.requireContext().getPackageName()));
        ammo_icon.setImageResource(this.requireContext().getResources().getIdentifier(weapon.getAmmo_icon(), "mipmap", this.requireContext().getPackageName()));
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity()).setCustomTitle(title);

        View dialogView = inflater.inflate(R.layout.dialog_view_weapon, null);
        ImageView screenshot = dialogView.findViewById(R.id.imageViewScreenshot);
        TextView synergyTextView = dialogView.findViewById(R.id.textViewSynergy);
        Button buttonClose = dialogView.findViewById(R.id.buttonClose);
        if (weapon.getSynergy().equals("set()"))
            synergyTextView.setText("No synergistic combinations available.");
        else synergyTextView.setText(weapon.getSynergy());
        screenshot.setImageResource(this.requireContext().getResources().getIdentifier(weapon.getScreenshot(), "drawable", this.requireContext().getPackageName()));
        if(!weapon.getPerk_column_1().equals("'Static'")) {
            String[] perk_column_1 = weapon.getPerk_column_1().split(", ");
            String[] perk_column_2 = weapon.getPerk_column_2().split(", ");
            String[] perk_column_3 = weapon.getPerk_column_3().split(", ");
            String[] perk_column_4 = weapon.getPerk_column_4().split(", ");
            String[][] perks = {perk_column_1, perk_column_2, perk_column_3, perk_column_4};
            RadioGroup[] rg = {dialogView.findViewById(R.id.rg1),
                    dialogView.findViewById(R.id.rg2),
                    dialogView.findViewById(R.id.rg3),
                    dialogView.findViewById(R.id.rg4)};
            for (int i = 0; i < perks.length; i++) {
                for (int j = 0; j < perks[i].length; j++) {
                    RadioButton temp = new RadioButton(this.requireContext());
                    temp.setContentDescription(perks[i][j]);
                    int id = this.requireContext().getResources().getIdentifier(dataAdapter.selectPerk(perks[i][j].substring(1, perks[i][j].length() - 1)), "mipmap", this.requireContext().getPackageName());
                    temp.setForeground(getResources().getDrawable(id));
                    temp.setBackgroundResource(R.drawable.perk_background);
                    temp.setGravity(Gravity.CENTER);
                    temp.setTag(id);

                    RadioGroup.LayoutParams params = new RadioGroup.LayoutParams(130, 130);
                    params.setMargins(0, 5, 0, 5);
                    temp.setLayoutParams(params);
                    temp.setButtonDrawable(R.drawable.transparent);
                    rg[i].addView(temp);
                    if (j == 0) rg[i].check(temp.getId());
                }
            }




            Cursor cursor = dataAdapter.selectRolls(weapon.getName());
            LinearLayout ll = dialogView.findViewById(R.id.table);
            while (cursor.moveToNext()) {
                LinearLayout row = new LinearLayout(requireContext());
                for (int i = 1; i < 5; i++) {
                    ImageView iv = new ImageView(requireContext());
                    iv.setImageResource(cursor.getInt(i));
                    iv.setLayoutParams(new LinearLayout.LayoutParams(130, 130, 1));
                    row.addView(iv);
                }
                Button button = new Button(requireContext());
                button.setBackgroundResource(R.drawable.x);
                button.setOnClickListener(view -> {
                    Cursor temp_cursor = dataAdapter.selectRolls(weapon.getName());
                    temp_cursor.moveToPosition((Integer) row.getTag());
                    ll.removeView(row);
                    dataAdapter.removeRoll(weapon.getName(), temp_cursor.getInt(1), temp_cursor.getInt(2), temp_cursor.getInt(3), temp_cursor.getInt(4));
                    temp_cursor.close();
                });
                LinearLayout.LayoutParams parameters = new LinearLayout.LayoutParams(10, 70, 0.6f);
                parameters.setMargins(0, 0, 10, 0);
                button.setLayoutParams(parameters);
                button.setGravity(Gravity.CENTER_VERTICAL);
                row.addView(button);
                row.setGravity(Gravity.CENTER_VERTICAL);
                row.setTag(cursor.getPosition());
                ll.addView(row);
            }
            cursor.close();
            Button buttonSave = dialogView.findViewById(R.id.save_button);
            buttonSave.setOnClickListener(v -> {

                LinearLayout row = new LinearLayout(requireContext());
                int[] ids = new int[4];
                for (int i = 0; i < rg.length; i++) {
                    RadioButton temp = dialogView.findViewById(rg[i].getCheckedRadioButtonId());
                    ImageView iv = new ImageView(requireContext());
                    ids[i] = (Integer) temp.getTag();
                    iv.setImageResource(ids[i]);
                    iv.setLayoutParams(new LinearLayout.LayoutParams(130, 130, 1));
                    row.addView(iv);
                }
                Button button = new Button(requireContext());
                button.setBackgroundResource(R.drawable.x);
                button.setOnClickListener(view -> {
                    Cursor temp_cursor = dataAdapter.selectRolls(weapon.getName());
                    temp_cursor.moveToPosition((Integer) row.getTag());
                    ll.removeView(row);
                    dataAdapter.removeRoll(weapon.getName(), ids[0], ids[1], ids[2], ids[3]);
                });
                LinearLayout.LayoutParams parameters = new LinearLayout.LayoutParams(10, 70, 0.6f);
                parameters.setMargins(0, 0, 10, 0);
                button.setLayoutParams(parameters);
                button.setGravity(Gravity.CENTER_VERTICAL);
                row.addView(button);
                row.setGravity(Gravity.CENTER_VERTICAL);
                Cursor temp_cursor = dataAdapter.selectRolls(weapon.getName());
                row.setTag(temp_cursor.getCount());
                temp_cursor.close();
                ll.addView(row);
                dataAdapter.insertRoll(weapon.getName(), ids[0], ids[1], ids[2], ids[3]);
            });
        }
        builder.setView(dialogView).setMessage(" ");
        buttonClose.setOnClickListener(view -> {

            dismiss();
        });
        return builder.create();
    }

    public void sendSelectedWeapon (Weapon weapon) {
        this.weapon = weapon;
    }
}
