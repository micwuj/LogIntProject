package com.example.loginttester2;

public class Record {
    private String sdriver;
    private String spackage;
    private String saction;
    private String sdate;

    public Record() {

    }
    public Record(String sdriver, String spackage, String saction, String sdate) {
        this.sdriver = sdriver;
        this.spackage = spackage;
        this.saction = saction;
        this.sdate = sdate;
    }

    public String getSdriver() {
        return sdriver;
    }

    public String getSpackage() {
        return spackage;
    }

    public String getSaction() {
        return saction;
    }

    public String getSdate() {
        return sdate;
    }

    public void setSdriver(String sdriver) {
        this.sdriver = sdriver;
    }

    public void setSpackage(String spackage) {
        this.spackage = spackage;
    }

    public void setSaction(String saction) {
        this.saction = saction;
    }

    public void setSdate(String sdate) {
        this.sdate = sdate;
    }
}
