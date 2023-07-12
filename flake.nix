{
  inputs = {
    nixpkgs.url = "github:ckiee/nixpkgs/kag-unbork";
    #nixpkgs.url = "github:NixOS/nixpkgs/2043dbb6faa9e21b0fb500161542e30d6c8bc680";
    flake-utils.url = "github:numtide/flake-utils";
    mynur.url = "github:Lykos153/nur-packages";
    mynur.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, flake-utils, mynur }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ mynur.overlay ];
        };
        
        my-python = pkgs.python3.override {
          packageOverrides = (pyfinal: pyprev: {
            kaldi-active-grammar = pyprev.kaldi-active-grammar.overrideAttrs (old: {
              patches = old.patches ++ [
                ./004-fix-alternative-dictation.patch            
              ];
            });
          });
        };
        python-with-my-packages = my-python.withPackages (p: with p; [
          dragonfly
          kaldi-active-grammar
          pkgs.lykos153.python3Packages.g2p-en
        ]);
        kaldi-ag-simple = pkgs.stdenv.mkDerivation {
          name = "kaldi-ag-simple";
          pname = "kaldi_module_loader_plus.py";
          propagatedBuildInputs = [
            python-with-my-packages
          ];
          dontUnpack = true;
          installPhase = ''
            for f in _all.py  _dictation.py  keyboard.py  mode.py  programs.py  tformat.py  words.py; do
              install -Dm644 ${./.}/$f $out/bin/$f
            done
            install -Dm755 ${./.}/kaldi_module_loader_plus.py $out/bin/kaldi_module_loader_plus.py
          '';
        };
        kaldi-ag-with-model = pkgs.writeShellScriptBin "kaldi-ag-with-model" ''
          set -x
          kaldi_dir=$HOME/.local/share/kaldi-ag-with-model
          mkdir -p "$kaldi_dir" &&
          chmod -R +rwx "$kaldi_dir" &&
          rm -rf "$kaldi_dir" &&
          mkdir -p "$kaldi_dir" &&
          cd "$kaldi_dir" &&
          cp -rs ${kaldi-model-daanzu-biglm} ./kaldi_model &&
          chmod +rwx "./kaldi_model/" &&
          for fn in user_lexicon.txt words.txt align_lexicon.int lexiconp_disambig.txt L_disambig.fst; do
            rm -f "./kaldi_model/$fn"
            cp "${kaldi-model-daanzu-biglm}/$fn" "./kaldi_model/$fn"
            chmod +w "./kaldi_model/$fn"
          done &&

          exec ${kaldi-ag-simple}/bin/kaldi_module_loader_plus.py
        '';
        kaldi-model-daanzu-smalllm = pkgs.fetchzip
          {
            url = https://github.com/daanzu/kaldi-active-grammar/releases/download/v3.0.0/kaldi_model_daanzu_20211030-smalllm.zip;
            hash = "sha256-qIqzGR4La78oPaVd6fqARgh8oH6ozzBLc1tcG2AVILU=";
          };
        kaldi-model-daanzu-mediumlm = pkgs.fetchzip
          {
            url = https://github.com/daanzu/kaldi-active-grammar/releases/download/v3.0.0/kaldi_model_daanzu_20211030-mediumlm.zip;
            hash = "sha256-PjBBW81W5uumpkxnhn7DAV2A0yemGoAW0Z4M5D+P5E8=";
          };
        kaldi-model-daanzu-biglm = pkgs.fetchzip
          {
            url = https://github.com/daanzu/kaldi-active-grammar/releases/download/v3.0.0/kaldi_model_daanzu_20211030-biglm.zip;
            hash = "sha256-5AIir7D7/krNpvR3atCgUZgM6HwPk7CXiTtym4BjxsQ=";
          };

      in {
        packages = {
          inherit kaldi-ag-simple;
          inherit kaldi-ag-with-model;
        };
        defaultPackage = kaldi-ag-with-model;
        devShell = pkgs.mkShell {
         packages = [
           python-with-my-packages
         ];
        };
      });
}
