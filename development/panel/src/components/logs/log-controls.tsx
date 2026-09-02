"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { validateLogLines } from "@/lib/utils/validation";

interface LogControlsProps {
  lines: number;
  onChange: (lines: number) => void;
}

export function LogControls({ lines, onChange }: LogControlsProps) {
  const [customLines, setCustomLines] = useState(String(lines));

  const handleBlur = () => {
    const parsed = parseInt(customLines, 10);
    if (Number.isNaN(parsed)) {
      setCustomLines(String(lines));
      return;
    }
    const validation = validateLogLines(parsed);
    if (!validation.valid) {
      setCustomLines(String(lines));
      return;
    }
    onChange(parsed);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleBlur();
    }
  };

  const presets = [100, 500, 1000, 2000];

  return (
    <div className="flex flex-wrap items-end gap-3">
      <div>
        <Label className="text-xs text-muted-foreground">Presets</Label>
        <div className="flex flex-wrap gap-1.5 mt-1">
          {presets.map((preset) => (
            <Button
              key={preset}
              variant={lines === preset ? "default" : "outline"}
              size="sm"
              onClick={() => {
                onChange(preset);
                setCustomLines(String(preset));
              }}
            >
              {preset}
            </Button>
          ))}
        </div>
      </div>

      <div className="flex flex-col">
        <Label htmlFor="custom-lines">Custom Lines</Label>
        <Input
          id="custom-lines"
          type="number"
          min={1}
          max={5000}
          value={customLines}
          onChange={(e) => setCustomLines(e.target.value)}
          onBlur={handleBlur}
          onKeyDown={handleKeyDown}
          className="w-24"
        />
      </div>
    </div>
  );
}
