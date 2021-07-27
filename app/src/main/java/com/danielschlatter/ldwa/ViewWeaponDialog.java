package com.danielschlatter.ldwa;

import android.app.AlertDialog;
import android.app.Dialog;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.DialogFragment;

import java.util.Objects;

public class ViewWeaponDialog extends DialogFragment {
    private Weapon weapon;
    public ViewWeaponDialog() {}
    @NonNull
    @Override
    public Dialog onCreateDialog(@Nullable Bundle savedInstanceState) {
        Dialog dialog = super.onCreateDialog(savedInstanceState);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialog.setCanceledOnTouchOutside(true);
        LayoutInflater inflater = requireActivity().getLayoutInflater();
        View dialogView = inflater.inflate(R.layout.dialog_view_weapon, null);
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity()).setTitle(weapon.getName());
        //Declare variables to hold reference to EditText used for collecting data
        ImageView screenshot = dialogView.findViewById(R.id.imageViewScreenshot);
        TextView typeTextView = dialogView.findViewById(R.id.textViewType);
        TextView archetypeTextView = dialogView.findViewById(R.id.textViewArchetype);
        ImageView icon = dialogView.findViewById(R.id.imageViewIcon);
        TextView elementTextView = dialogView.findViewById(R.id.textViewElement);
        TextView slotTextView = dialogView.findViewById(R.id.textViewSlot);
        TextView ammoTextView = dialogView.findViewById(R.id.textViewAmmo);
        ImageView ammo_icon = dialogView.findViewById(R.id.imageViewAmmo_icon);
        TextView synergyTextView = dialogView.findViewById(R.id.textViewSynergy);
        TextView perk_column_1TextView = dialogView.findViewById(R.id.textViewPerk_column_1);
        TextView perk_column_2TextView = dialogView.findViewById(R.id.textViewPerk_column_2);
        TextView perk_column_3TextView = dialogView.findViewById(R.id.textViewPerk_column_3);
        TextView perk_column_4TextView = dialogView.findViewById(R.id.textViewPerk_column_4);
        ImageView element_icon = dialogView.findViewById(R.id.imageViewElement_icon);
        Button buttonClose = dialogView.findViewById(R.id.buttonClose);
        typeTextView.setText(weapon.getType());
        archetypeTextView.setText(weapon.getArchetype());

        icon.setImageResource(this.requireContext().getResources().getIdentifier(weapon.getIcon(), "mipmap", this.requireContext().getPackageName()));
        elementTextView.setText(weapon.getElement());
        slotTextView.setText(weapon.getSlot());
        ammoTextView.setText(weapon.getAmmo());
        ammo_icon.setImageResource(this.requireContext().getResources().getIdentifier(weapon.getAmmo_icon(), "mipmap", this.requireContext().getPackageName()));
        synergyTextView.setText(weapon.getSynergy());
        perk_column_1TextView.setText(weapon.getPerk_column_1());
        perk_column_2TextView.setText(weapon.getPerk_column_2());
        perk_column_3TextView.setText(weapon.getPerk_column_3());
        perk_column_4TextView.setText(weapon.getPerk_column_4());
        screenshot.setImageResource(this.requireContext().getResources().getIdentifier(weapon.getScreenshot(), "drawable", this.requireContext().getPackageName()));
        element_icon.setImageResource(this.requireContext().getResources().getIdentifier(weapon.getElement_icon(), "mipmap", this.requireContext().getPackageName()));
        builder.setView(dialogView).setMessage(" ");
        buttonClose.setOnClickListener(view -> dismiss());
        return builder.create();
    }

    public void sendSelectedWeapon (Weapon weapon) {
        this.weapon = weapon;
    }
}
